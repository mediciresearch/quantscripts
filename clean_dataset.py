from multiprocessing import Pool, cpu_count, Manager, current_process
from rapidfuzz import fuzz
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(processName)s: %(message)s',
)

def contains_similar_text(text, titles, threshold=90):
    for title in titles:
        similarity_score = fuzz.partial_ratio(title.lower(), text.lower())
        if similarity_score >= threshold:
            logging.info(f"Text: {text[:30]}... matched title: {title} with a score of {similarity_score}")
            return True
    return False


def process_record(args):
    record, titles = args
    text = record.get('text', '')
    if not contains_similar_text(text, titles):
        return record
    return None

def init_worker():
    # This will make sure that each worker initializes the logging system
    logging.getLogger().setLevel(logging.INFO)

def main(input_file, output_file, titles_file):
    logging.info("Loading title filters...")
    with open(titles_file, 'r') as f:
        titles = [line.strip() for line in f]
        logging.info(f"Loaded {len(titles)} titles to filter out.")

    logging.info("Initializing multiprocessing resources...")
    manager = Manager()
    records_to_write = manager.list()

    num_processes = cpu_count()
    logging.info(f"Number of processes: {num_processes}")

    logging.info("Starting the record filtering process...")
    try:
        with Pool(processes=num_processes, initializer=init_worker) as pool:
            with open(input_file, 'r') as f:
                # Debug: Read first line to check file and JSON format
                first_line = next(f, None)
                if first_line:
                    try:
                        first_record = json.loads(first_line)
                        logging.info(f"First record loaded for testing: {first_record}")
                    except json.JSONDecodeError as e:
                        logging.error(f"JSON decode error on first line: {e}")
                        return
                
                f.seek(0)  # Reset file pointer to the start

                records = (json.loads(line) for line in f)
                chunksize = 10  # Adjust as needed
                for result in pool.imap_unordered(process_record, ((record, titles) for record in records), chunksize=chunksize):
                    if result:
                        records_to_write.append(result)
                    else:
                        logging.debug("A record was filtered out by the matching condition.")
    except Exception as e:
        logging.error(f"An error occurred during multiprocessing: {e}")
        raise

    logging.info("Finished filtering, now writing results...")
    if records_to_write:
        logging.info(f"{len(records_to_write)} records ready to be written.")
        with open(output_file, 'w', buffering=1<<16) as f:
            for record in records_to_write:
                f.write(json.dumps(record) + '\n')
        logging.info(f"Written record to {output_file}")
    else:
        logging.warning("No records were added to the write queue. Check the filters and data processing logic.")

    

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        logging.error("Usage: python script.py input_jsonl_file output_jsonl_file titles_file")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        titles_file = sys.argv[3]
        logging.info("Script started")
        main(input_file, output_file, titles_file)
        logging.info("Script finished")