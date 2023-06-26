import os
import streamlit as st
import cv2
from tensorflow import keras
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
model = keras.models.load_model('pages/VGG19_softmax.h5')
###################| Function |#########################################################
st.set_page_config(
    page_title="Predict",
    page_icon="👋",
)

st.sidebar.write("# Predict")


def LoadImage(path: str) -> list:
    allfiles = os.listdir(path)
    images = []
    for file in allfiles:
        images.append(file)
    return images

def remove(path: str) -> None:
    for file in os.listdir(path):
        os.remove(os.path.join(path,file))

def formatData(images):
    img_size = 450
    data = []
    for path,sabdirname,filename in os.walk(images):                       
        for file in filename:   
            img_path = os.path.join(path,file)
            img_array = cv2.imread(img_path)
            if img_array is None:
                continue 
            img_resize = cv2.resize(img_array, (img_size, img_size))
            data.append(img_resize)   
    return data

def Predict(image):
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    predict_image = model.predict(image)
    classe_predite = np.argmax(predict_image)
    if classe_predite == 0:
        return ("AFS",predict_image)
    elif classe_predite == 1:
        return ("AFC",predict_image)
    elif classe_predite == 2:
        return ("AF",predict_image)
    elif classe_predite == 3:
        return ("AFSC",predict_image)
    elif classe_predite == 4:
        return ("FSC",predict_image)
    elif classe_predite == 5:
        return ("FS",predict_image)
    elif classe_predite == 6:
        return ("FC",predict_image)
    else:
        return "NC"

st.markdown('''<h2 style="color:#333333;">PREDICTEUR</h2> ''',unsafe_allow_html=True)
st.info(''' ❓  Le principe de la version bêta du prédicteur exige de uploader un seul fichier image, puis d'appuyer sur le bouton de prédiction. Après la prédiction, appuyez sur remove pour suprimer l'image et ensuite re-uploader une image pour tester à nouveau. Répétez cette même procédure pour chaque image à tester.''',)
listelementsorted=sorted(os.listdir("./pages/images/"))
newlistelement = []
pathimagenew = []
for i in range(len(listelementsorted)):
    if "controle11l" in str(listelementsorted[i]) :
        newlistelement.insert(10,listelementsorted[-4])
    elif "controle1r" in str(listelementsorted[i]):
        newlistelement.insert(35,listelementsorted[-3])
    elif "controle21r" in str(listelementsorted[i]):
        newlistelement.insert(55,listelementsorted[-2])
    elif "controle36l" in str(listelementsorted[i]):
        newlistelement.insert(35,listelementsorted[-1])
    else:
        newlistelement.insert(i,listelementsorted[i])

for el in newlistelement:
    pathimagenew.append("./pages/images/"+str(el))

    
try:
    dfleft = pd.read_csv("pages/xlsx/left.csv")
    dfright = pd.read_csv("pages/xlsx/right.csv")
    frames = [dfleft, dfright]
    result = pd.concat(frames)
except FileNotFoundError:
    st.error("Crop image !!!")
vector = np.vectorize(np.float_)
predictionlist = []
if st.button("Predict"):
    st.write("")
    data = formatData("./pages/images/")
    allimagespath = pathimagenew
    collabel,col2label,col3label= st.columns(3)
    with collabel:
        st.write("##### Image")
    with col2label:
        st.write("##### Predict")
    with col3label:
        st.write("##### Plot the class probability")
    st.markdown('''<hr style="border-top: 3px solid #333333;">''',unsafe_allow_html=True)
    for i in range(len(allimagespath)):
        col,col2,col3= st.columns(3)
        prediction = Predict(data[i])
        with col:
            image =st.image(allimagespath[i],caption=str(allimagespath[i]).replace("Gel_IEF2023","").replace(".jpg",""))
        with col2:
            st.write(prediction[0])
            predictionlist.append(prediction[0])
        #listimage.append(str(image))
        #listpredict.append(prediction)
        with col3:
            fig, ax = plt.subplots()
            axes = ["AFS","AFC","AF","AFSC","FSC","FS","FC","NC"]
            ax.bar(axes,vector(prediction[1]).tolist()[0])
            st.pyplot(fig)
        st.markdown('''<hr style="border-top: 3px solid #333333;">''',unsafe_allow_html=True)
    result["Prediction"]=predictionlist
    st.table(result.iloc[:,1:])
    result.iloc[:,1:].to_excel("pages/downloadfile/downloadfileresult.xlsx",index=False)
if os.path.exists("pages/downloadfile/downloadfileresult.xlsx"):
    with open("pages/downloadfile/downloadfileresult.xlsx", "rb") as file:
            btn = st.download_button(
                label="Download result.xlsx",
                data=file,
                file_name="result.xlsx",
                mime="text/xlsx"
              )


st.write("")
if st.button("remove"):
    remove('./pages/images/')
    remove("./pages/xlsx/")
    remove("./pages/downloadfile/")

   