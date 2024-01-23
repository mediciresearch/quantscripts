const fs = require("fs");
const path = require("path");

// Directory from which to list files
const directoryPath = "../notion"; // Replace with your directory path

// Text file where the names will be saved
const outputFilePath = "./quantTextbookNames.txt";

// Read directory
fs.readdir(directoryPath, (err, files) => {
  if (err) {
    return console.error("Unable to read directory: " + err);
  }

  // Create a string with all the file names
  const fileNames = files.join("\n");

  // Write to the text file
  fs.writeFile(outputFilePath, fileNames, (err) => {
    if (err) {
      return console.error("Error writing to file: " + err);
    }
    console.log("File names have been written to " + outputFilePath);
  });
});
