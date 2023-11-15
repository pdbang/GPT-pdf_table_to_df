import numpy as np
import streamlit as st
from PIL import Image
from pdf2jpg import pdf2jpg
import os, shutil, uuid

FOOTER_ROWS = 300
WHITE_VALUE = 255

def try_remove(path: str) -> None:
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

def create_tmp_sub_folder() -> str:
    """
    Creates a temporary sub folder under tmp

    :return:
    """
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    tmp_sub_folder_name = str(uuid.uuid4())[:8]
    tmp_sub_folder_path = os.path.join("tmp", tmp_sub_folder_name)
    os.mkdir(tmp_sub_folder_path)
    return tmp_sub_folder_path

def crop_white_space(arr: np.array) -> np.array:
    white_pixels = (arr == WHITE_VALUE)
    white_rows = list(np.all(white_pixels, axis=(1, 2)))
    last_non_white_row_idx = max(loc for loc, val in enumerate(white_rows) if not val)
    merged_arr = arr[:last_non_white_row_idx + FOOTER_ROWS]
    return merged_arr

def display_pdf(file):
        # Create temporary folder for generated image
        tmp_sub_folder_path = create_tmp_sub_folder()
        with open(file.name, "wb") as f:
            f.write(file.getvalue())
        # Save images in that sub-folder
        result = pdf2jpg.convert_pdf2jpg(file.name, tmp_sub_folder_path, pages="ALL")
        # if result:
        images = []
        for image_path in result[0]["output_jpgfiles"]:
            images.append(np.array(Image.open(image_path)))

        # Create merged image from all images + remove irrelevant whitespace
        merged_arr = np.concatenate(images)
        merged_arr = crop_white_space(merged_arr)
        merged_path = os.path.join(tmp_sub_folder_path, "merged.jpeg")
        Image.fromarray(merged_arr).save(merged_path)

        css='''
        <style>
            [data-testid="stImage"]{
                overflow: scroll;
                height: 200px;
            }
        </style>
        '''

        st.markdown(css, unsafe_allow_html=True)


        # Display the image
        st.image(merged_path)
                
        try_remove(tmp_sub_folder_path)