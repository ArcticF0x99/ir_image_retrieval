from pathlib import Path
from glob import glob
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

DATASET_PATH = 'dataset23'
QREL_PATH = 'out/run*.txt'
TARGET_PATH = 'doccano'

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def load_queries_xml():
    file_name = glob(DATASET_PATH + '/*.xml')[0]
    
    topics = pd.read_xml(file_name)
    
    ret = pd.DataFrame()
    # https://github.com/terrier-org/pyterrier/issues/62\n",
    ret['query'] = topics['title'].apply(lambda i: "".join([x if x.isalnum() else " " for x in i]))
    ret['qid'] = topics['number']
    return ret

def load_queries_jsonl():
    file_name = glob(DATASET_PATH + '/*.jsonl')[0]
    return pd.read_json(file_name, lines=True)

def load_queries() -> pd.DataFrame:
    try:
        return load_queries_xml()
    except:
        pass
    
    try:
        return load_queries_jsonl()
    except:
        pass
    
    raise Exception(f'Found no topics file. Got: {glob(DATASET_PATH + "/*")}')

def add_subtitle(
    bg,
    text="nice",
    xy=("center", 2),
    font="arial.ttf",
    font_size=53,
    font_color=(255, 255, 255),
    stroke=2,
    stroke_color=(0, 0, 0),
    shadow=(4, 4),
    shadow_color=(0, 0, 0),
):
    """draw subtitle on image by pillow
    Args:
        bg(PIL image): image to add subtitle
        text(str): subtitle
        xy(tuple): absolute top left location of subtitle
        ...: extra style of subtitle
    Returns:
        bg(PIL image): image with subtitle
    """
    stroke_width = stroke
    xy = list(xy)
    W, H = bg.width, bg.height
    font = ImageFont.truetype(str(font), font_size)
    w, h = font.getsize(text, stroke_width=stroke_width)
    
    target_image_width = w * 1.2
    scale = target_image_width / W
    if scale > 1:
        bg = bg.resize((int(scale * W), int(scale * H)), Image.Resampling.LANCZOS)

    bg = ImageOps.expand(bg, border=(0, 60, 0, 0), fill=(0,0,0))
    W, H = bg.width, bg.height

    if xy[0] == "center":
        xy[0] = (W - w) // 2
    if xy[1] == "center":
        xy[1] = (H - h) // 2
    draw = ImageDraw.Draw(bg)
    if shadow:
        draw.text(
            (xy[0] + shadow[0], xy[1] + shadow[1]), text, font=font, fill=shadow_color
        )
    draw.text(
        (xy[0], xy[1]),
        text,
        font=font,
        fill=font_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color,
    )
    return bg

x = glob(DATASET_PATH+'/images/*')[0].split('\\')[-1]
first_directory_len = len(glob(DATASET_PATH+'/images/*')[0].split('\\')[-1])
print(glob(QREL_PATH))

results_df = pd.concat((pd.read_csv(path, sep=' ', header=None) for path in glob(QREL_PATH)), ignore_index=True)  
relevant_image_ids = results_df[[0,2]]
print(relevant_image_ids.shape)
print(relevant_image_ids.drop_duplicates().shape)

queries = load_queries().set_index('qid')
Path(TARGET_PATH).mkdir(parents=True, exist_ok=True)
for topic_id, image_id in relevant_image_ids.itertuples(index=False):
    image_path = DATASET_PATH + '/images/' + image_id[:first_directory_len] + '/' + image_id + '/image.webp'
    image = Image.open(image_path).convert('RGB')
    image = add_subtitle(image, queries.loc[topic_id]['query'])
    image.save(TARGET_PATH  + '/' + str(topic_id) + '-' + image_id + '.jpg', 'jpeg')