# module importation
import streamlit as st
from PIL import Image
import pandas as pd
import os
import random



st.set_page_config(page_title="Data Upload", page_icon="📈")

st.markdown("# Upload Data")
st.sidebar.header("Data Upload")
st.write(
    """Descriptif"""
)
def save_uploadedfileref(uploadedfile):
    with open(os.path.join("pages/xlsx",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())


def image_crop(New_image,nbSubdivition : int = 36) -> list:
      img  = New_image 
      sub = []
      for i in range(nbSubdivition):
          sub.append(img.crop((0,(img.size[1]/nbSubdivition)*i,img.size[0],((img.size[1]/nbSubdivition)*(i+1)))))
      return sub


# function for save all images
def saveAllImage(numeroCalque : str,sub : list,idregistre : list,imagePart : str) -> None:
        for i in range(len(sub)):
            if imagePart == 'left':
                if str(idregistre[i]) == 'Contrôle':
                    sub[i].save('./pages/images/'+numeroCalque+"controle"+str(i+1)+'l.jpg')
                else:
                    sub[i].save('./pages/images/'+numeroCalque+str(idregistre[i])+'.jpg')
            else:
                if str(idregistre[i]) == 'Contrôle':
                    sub[i].transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(
                    './pages/images/'+numeroCalque+"controle"+str(i+1)+'r.jpg')
                else:
                     sub[i].transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(
                    './pages/images/'+numeroCalque+str(idregistre[i])+'.jpg')

# function get root path and subdirectories
def get_all_file_paths(directory):
  
    # initializing empty file paths list
    file_paths = []
  
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
  
    # returning all file paths
    return file_paths  

colparametre, colimage, colsub = st.columns([3,1,1])
# section to apply cropping image and save...
with colparametre:
    with st.expander('Parameters',expanded=True):
        nom_calque = st.text_input('Layer name:',placeholder="date_Gxx")
        file = st.file_uploader("Import image :",type=['png','jpg'])
        subdivised = st.number_input('Subdivision number',step=1,min_value=8,max_value=36,value=36)
        filexlsx = st.file_uploader('Import excel file :',type='xlsx')

    sub=[]
    
    if file != None:
        image = Image.open(file)
        imagepart = st.radio('Right or left image',options=['left','right'])
        if imagepart == 'left':
            w,h= image.size
            crop_left = st.slider('left',min_value=0,max_value=w,value=260)
            crop_top = st.slider('top',min_value=0,max_value=h,value=350)
            crop_right = st.slider('right',min_value=0, max_value=w,value=645)
            crop_bottom = st.slider('bottom',min_value=0,max_value=h,value=1988)
            if (crop_left < crop_right and crop_bottom > crop_top):
                NewImage = image.crop((crop_left,crop_top,crop_right,crop_bottom))
                st.write(NewImage.size)
                if NewImage.size[0] < image.size[0] and NewImage.size[1] < image.size[1]:
                    st.info("Resolution acceptable")
                    sub = image_crop(NewImage,subdivised)
                    if filexlsx != None:
                        df = pd.read_excel(filexlsx)
                        if st.button('Save'):
                            excel_left_id = df.iloc[:36,-3]
                            try:
                                saveAllImage(nom_calque,sub,excel_left_id.to_list(),imagepart)
                                df.iloc[:subdivised,0:3].to_csv("pages/xlsx/left.csv")
                                st.success("carry out")
                            except:
                                st.warning('error')
                else:
                    st.warning("Adjusted the image")
            else:
                st.warning("Adjusted the image")
        else:
            w,h= image.size
            crop_left = st.slider('left',min_value=0,max_value=w,value=1023)
            crop_top = st.slider('top',min_value=0,max_value=h,value=350)
            crop_right = st.slider('right',min_value=0, max_value=w,value=1410)
            crop_bottom = st.slider('bottom',min_value=0,max_value=h,value=1984)
            if (crop_right > crop_left and crop_bottom > crop_top):
                NewImage = image.crop((crop_left,crop_top,crop_right,crop_bottom))
                st.write(NewImage.size)
                if NewImage.size[0] < image.size[0] and NewImage.size[1] < image.size[1]:
                    st.info("Resolution acceptable")
                    sub = image_crop(NewImage,subdivised)
                    if filexlsx != None:
                        df = pd.read_excel(filexlsx)
                        if st.button('Save'):
                            excel_rigth_id = df.iloc[36:,-3]
                            try:
                                saveAllImage(nom_calque,sub,excel_rigth_id.to_list(),imagepart)
                                df.iloc[subdivised:,0:3].to_csv("pages/xlsx/right.csv")
                                st.success("carry out")
                            except:
                                st.warning('error')
                else:
                    st.warning("Adjusted the image")
            else:
                st.warning("Adjusted the image")
    else:
        with st.expander('How to use ?'):
            st.markdown("The application is very simple to use enter the name of the layer, load the image as well as the excel file which is associated with it then check that there is no resolution error while this error will appear adjust the image once Once you adjust the image, you can crop it, don't forget to look at the end section which shows the portion of an image to be cropped, if the portion does not suit you adjust the image, then click save to apply the cut. As in general our images are in two parts, you will do the same exercise from left to right. Then at the top left you have a sidebar for exporting all the images.")

# columns for visualized adjusted image
with colimage:
    if file != None: 
        if crop_left < crop_right and crop_top < crop_bottom :
            st.image(NewImage)
# columns for visualized one random image crop
with colsub:
    if file != None and len(sub) != 0:
        st.markdown('### observe the cut :')
        choix = sub[0]
        if st.button('Next'):
            choix = random.choice(sub)
        st.image(choix)
