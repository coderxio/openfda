from urllib import request
from datetime import datetime
import zipfile
from pathlib import Path


def main():
    # assign the name of the file that will be stored in the data/ directory.
    # current output: data/2020-05-22_fda_data.zip 
    data_filename = f"{Path.cwd() / 'data' / str(datetime.date(datetime.now()))}_fda_data.zip"

    # get file content from the url
    file = request.urlopen("https://download.open.fda.gov/drug/ndc/drug-ndc-0001-of-0001.json.zip")

    # open a new file and write the data in the assigned folder
    with open(data_filename,'wb') as output:
      output.write(file.read())

    # unzip the file in the assigned folder
    with zipfile.ZipFile(data_filename,"r") as zip_ref:
        zip_ref.extractall(f"{Path.cwd() / 'data'}")

    # rename file to align with current code
    p = Path.cwd() / 'data' / 'drug-ndc-0001-of-0001.json'
    new_name = Path.cwd() / 'data' / 'drug-ndc.json'
    p.rename(new_name)


if __name__ == "__main__":
    main()
    