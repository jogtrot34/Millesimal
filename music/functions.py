import eyed3
from eyed3.id3.frames import ImageFrame


def embed_cover_art(audio_path, image_path):
    audiofile = eyed3.load(audio_path)
    if audiofile.tag is None:
        audiofile.initTag()

    with open(image_path, 'rb') as img_file:
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, img_file.read(), 'image/jpeg')

    audiofile.tag.save()
