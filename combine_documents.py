from pathlib import Path
import os
import tempfile
import win32api
import win32print
import PyPDF2
from PyPDF2 import PdfMerger
import time

files = []


# Recursively traverse entire folder structure (looks like preorder traversal)
def list_files_scandir(path='.'):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file() and '.pdf' in str(entry):
                # print(f"\n{entry.path}\n")
                # Add the filepath to the list to print
                files.append(entry.path)
            elif entry.is_dir():
                list_files_scandir(entry.path)

# I can automate this even further!
def merge_cover(filepath: str, number: str):
    merger2 = PdfMerger()

    merger2.append(f'{filepath}/Chandos Closeout Pages - Google Docs.pdf')
    merger2.append(f'{filepath}/combined.pdf')

    merger2.write(f'{filepath}/division{number.removeprefix('0')}.pdf')
    merger2.close()

    os.remove(f'{filepath}/Chandos Closeout Pages - Google Docs.pdf')
    os.remove(f'{filepath}/combined.pdf')

start = time.time()

merger = PdfMerger()

# Specify the directory path you want to start from
# for folder in folders:
directory_path = '../Combined PDFs/part1'
if os.path.exists(directory_path):
    print(os.listdir(directory_path))
list_files_scandir(directory_path)

for file in files:
    print(f"Attempting to merge: {file}")
    try:
        merger.append(file)
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error merging {file}: {e}")
    except PyPDF2.errors.DependencyError as e:
        print(f"Error: {e}. Skipping encrypted file: {file}")


print(f"\nNumber of files to be merged: {len(files)}\n")

# Loop through list and print the files

merger.write(f'../Combined PDFs/complete_architectural.pdf')
merger.close()

print(time.time() - start)
