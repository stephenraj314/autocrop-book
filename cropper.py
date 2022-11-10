import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path



def convert_to_images(pdf_file):

    Path("output/original/").mkdir(parents=True, exist_ok=True)
    Path("output/cropped/").mkdir(parents=True, exist_ok=True)

    command=["pdfimages","-j",pdf_file,"output/original/"]
    try:
        subprocess.run(command, check=True, timeout=60)
        print("Conversion from pdf to jpg done")
    except FileNotFoundError as e:
        print(
            f"Command {command} failed because the process "
            f"could not be found.\n{e}"
        )
    except subprocess.CalledProcessError as e:
        print(
            f"Command {command} failed "
            f"did not return a successful return code.\n{e}"
        )
    except subprocess.TimeoutExpired as e:
        print(f"Command {command} timed out.\n {e}")


def convert_to_pdf():
    root_dir = os.getcwd()
    input_path = os.path.join(root_dir,"output","cropped")
    os.chdir(input_path)
    org_files = [f"({x}) viewJPEG showpage" for x in os.listdir() if x.endswith(".jpg")]
    # using Ghostscript to convert image directory in pdf
    command=["gs","-q ","-dNOSAFER","-sPAPERSIZE=letter","-dNOPAUSE","-dBATCH",
    "-sDEVICE=pdfwrite",f"-sOutputFile={root_dir}/output.pdf","viewjpeg.ps","-c"]
    command = command + org_files

    try:
        subprocess.run(command, check=True, timeout=60)
        print("Conversion from jpg to pdf done")
    except FileNotFoundError as e:
        print(
            f"Command {command} failed because the process "
            f"could not be found.\n{e}"
        )
    except subprocess.CalledProcessError as e:
        print(
            f"Command {command} failed "
            f"did not return a successful return code.\n{e}"
        )
    except subprocess.TimeoutExpired as e:
        print(f"Command {command} timed out.\n {e}")


def autocrop_images():
    root_dir = os.getcwd()
    input_folder = os.path.join(root_dir,"output","original")
    orig_files = [x for x in os.listdir(input_folder) if x.endswith(".jpg")]
    for file in orig_files:
        input_path = os.path.join(root_dir,"output","original",file)
        output_path = os.path.join(root_dir,"output","cropped",file)
        command=["python","src/ndl-crop/ndl-crop/ndl-crop.py","-r",input_path,"-o",output_path]
        try:
            subprocess.run(command, check=True, timeout=60)
        except FileNotFoundError as e:
            print(
                f"Command {command} failed because the process "
                f"could not be found.\n{e}"
            )
        except subprocess.CalledProcessError as e:
            print(
                f"Command {command} failed "
                f"did not return a successful return code.\n{e}"
            )
        except subprocess.TimeoutExpired as e:
            print(f"Command {command} timed out.\n {e}")
    print("Images are cropped sucessfully")

if __name__ == "__main__":
    parser = ArgumentParser()
    #parser.add_argument("dir_path", type=str)
    parser.add_argument('--input', action='store', type=str,help="pdf file to autocrop")
    args = parser.parse_args()
    convert_to_images(args.input)
    autocrop_images()
    convert_to_pdf()
   
