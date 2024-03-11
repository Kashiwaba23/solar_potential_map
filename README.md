# 📚 Noboru

A data science app built using streamlit and deep learning.
In this project, we set out to use machine learning to identify viable rooftops which could be used to generate solar energy and contribute to the fight against climate change.

Using a prelabeled dataset provided by the Geospatial Information Authority of Japan (https://gisstar.gsi.go.jp/gsi-dataset/09/index.html), we retrained Meta's Segment Anything Model (SAM)
to identify rooftops.

One major issue we encountered with this dataset was that it only labeled 普通建物, i.e. all wooden buildings and any others which are less than three stories in height. This excludes
most apartment buildings, and virtually all large office buildings made with concrete. This fact significantly decreased overall model performance.

Due to limited time schedule and computational power, we were only able to retrain SAM in Pytorch for 10 epochs (took ~8 hours using GPU in Google Colab). This resulted in an F1 Score of around 32%, which then increased to around
66% after output smoothing using the maxflow python library.

We calculated the white space present in each output mask to calculate rooftop area. This area was then used to calculate solar power generation potentials as well as CO2 offset figures.

_DROP SCREENSHOT HERE_
<br>
App home: https://WHATEVER.herokuapp.com
   

## Getting Started
### Setup

Install requirements
```
pip install -r requirements.txt
```

### ENV Variables
Create `.env` file
```
touch .env
```
Inside `.env`, set these variables. For any APIs, see group Slack channel.
```
MAPS_API_KEY==your_own_key
API_RUN=LOCAL
MODEL_TARGET=local
```


## Built With
- [SAM](https://segment-anything.com/) - Base Model
- [PyTorch](https://pytorch.org/) - Model Re-Training
- [FastAPI](https://fastapi.tiangolo.com/) - Back-end API to process input images
- [Docker](https://www.docker.com/) - Container to host our API on the web
- [Streamlit](https://streamlit.io/) - Frontend
- [OpenCV](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) — For image processing and handling

## Acknowledgements
This project could not have been completed without tremendous help from my team mates and the Le Wagon TAs.

## Team Members
- [Sarah Underwood](https://github.com/sstollunderwood)
- [Mark Jarrett](https://github.com/jarrettm101)
- [Sam Wolf](https://github.com/SamWololo)
