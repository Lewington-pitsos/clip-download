# clip-download
 download images from LAION clip front
 
 
# Setup

This requires anaconda. Recommended if you want to keep your python install clean.

1. run setup.bat

2. create a shortcut for run.bat

3. edit the shortcut properties and in the target feild add cmd /k before the path (e.g. cmd /k "path\to\bat\file")

4. run the shortcut to open the console.

# Usage

1. Visit [Laion](https://rom1504.github.io/clip-retrieval/?back=https%3A%2F%2Fknn5.laion.ai&index=laion5B&useMclip=false)

2. put in a search, e.g. "cats"

3. download the JSON file

4. place the JSON file in the root of the repository 

5. create a new folder in the root called "hd"

5. type `python download.py` into the console and press enter.
