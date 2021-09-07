# BoxImageAnn
Create image annotations with boxes for desired objects

**BoxImageAnn** runs in your local machine and is based on OpenCV.

![Example](/figures/BoxImageAnn.png)


## Run BoxImageAnn

The main script is **ann.py** and it has some arguments:

```bash
python ann.py --folder test_images # <FOLDER WHERE THE IMAGES ARE IN>
```

```bash
python ann.py --folder test_images --extensions ['jpg', 'jpeg'] # <LIST OF EXTENSIONS FOR THE IMAGES>
```

```bash
python ann.py --folder test_images --extensions ['jpg', 'jpeg'] --names names.txt # <PATH TO THE FILE WITH THE OBJECTS LABELS>
```

```bash
python ann.py --folder test_images --extensions ['jpg', 'jpeg'] --names names.txt --max_side 750 # <MAXIMUM SIDE FOR DISPLAYING THE IMAGES>
```

## Evaluate the annotations

This repository also includes a jupyter notebook to check the annotations: [Test annotation notebook](/notebooks/Test%20annotations.ipynb)
