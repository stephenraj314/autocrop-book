import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path
import img2pdf

root_dir = os.getcwd()
print(root_dir)

def check_extension(file_name):
    if file_name.endswith('.pdf'):
        return True
    return False


def convert_to_images(pdf_file):
    '''Autocroping extracted images using cv2'''
    Path("output/original/").mkdir(parents=True, exist_ok=True)
    Path("output/cropped/").mkdir(parents=True, exist_ok=True)

    command=["pdfimages","-j",f"{root_dir}/{pdf_file}","output/original/"]
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
    '''Converting Cropped Images to PDF'''  
    input_path = os.path.join(root_dir,"output","cropped")
    image_files = [f"{input_path}/{x}" for x in os.listdir(input_path) if x.endswith(".jpg")]
    # using img2pdf to convert image directory in pdf
    pdf_bytes = img2pdf.convert(image_files)
    pdf_path = os.path.join(root_dir,"out-"+file_name)
    with open(pdf_path,"wb") as file:
        file.write(pdf_bytes)


def autocrop_images():
    '''Autocroping extracted images using cv2'''
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
    file_name = os.path.basename(args.input)
    if not check_extension(file_name):
        raise ValueError("Invalid input")
    convert_to_images(args.input)
    autocrop_images()
    convert_to_pdf()
   
