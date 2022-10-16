from importlib.resources import path
from PIL import Image, ImageDraw, ImageFont
from dimensions import *
import math
from pathlib import Path
import os.path


my_img = os.path.join('resources','wyr6.png')
fontf = ImageFont.truetype(font=os.path.join("fonts","opensans_bold.ttf"), size=36)

"""while True:
    sent = ''
    for i, w in enumerate(arr_a):
        lw = (len(sent+w)+1)*LETTER_WIDTH
        print(sent+w, lw)
        if (lw < box_width):
            sent = sent+w+' '
            if i == len(arr_a)-1:
                arr_sentences_a.append(sent.strip())
        else:
            sent = sent+w+' '
            arr_sentences_a.append(sent.strip())
            sent = ''
        if i == len(arr_a)-1:
            break
    break
"""


class FormWyr():
    """
    forms would you rather image

    """

    def __init__(self):
        self.frame = Image.open(my_img)
        self.image_editable = ImageDraw.Draw(self.frame)
        self.inline_spacing = 10
        self.margin = 20
        # removing margin from both sides
        self.box_width = int(BOX_WIDTH-self.margin*2)
        self.x_add = x_black1 + self.margin

    def form_sentences(self, sentence: str, image_editable: ImageDraw, boxwidth: int, font):
        """

        breaking the input sentence into 
        sentences which fit the box

        """
        arr_a = sentence.split(' ')
        j = 0
        arr_a2 = []
        while True:
            sent = ''
            while j < len(arr_a):
                w = arr_a[j]
                # (len(sent+w)+1)*LETTER_WIDTH
                lw = image_editable.textlength((sent+w), font=font)
                if (lw < boxwidth):
                    sent += w + ' '
                    if j == len(arr_a)-1:
                        arr_a2.append(sent.strip())
                else:
                    arr_a2.append(sent.strip())
                    sent = ''
                    j = j-1
                j += 1
            break
        return arr_a2

    def write_sentences(self, box_no: int, arr: list):
        """
        writing the sentences on the boxes

        """
        # making the y adjust based on number of sentences
        y = Y[box_no-1]-len(arr)*(LETTER_HEIGHT/2)
        for l in arr:
            text_width = self.image_editable.textlength(l, font=fontf)
            # space to add to center the text in the box
            space = int((self.box_width-text_width)/2)
            x = space + self.x_add
            self.image_editable.text((x, y), text=l, font=fontf)
            y += LETTER_HEIGHT + self.inline_spacing
            x = 0

    def get_image(self, a: str, b: str):
        ar = self.form_sentences(
            a, image_editable=self.image_editable, boxwidth=self.box_width, font=fontf)
        self.write_sentences(1, ar)
        ar2 = self.form_sentences(
            b, image_editable=self.image_editable, boxwidth=self.box_width, font=fontf)
        self.write_sentences(2, ar2)
        self.frame.save(os.path.join('resources', 'wyr_final.png'))


class GetWyrResultImg():
    """Get the result image for would you rather
    """

    def __init__(self, ch1: str, ch2: str, votes1: int, votes2: int):
        self.ch1 = ch1
        self.ch2 = ch2
        self.votes1 = votes1
        self.votes2 = votes2
        self.letter_height = 30
        self.fontq = ImageFont.truetype(font=os.path.join(
            'fonts', 'opensans_bold.ttf'), size=32)

    def form_block(self, box):
        if box == 1:
            vote = self.votes1
            pat = Path("resources/wyr_results/red_box_final.png")
            img_path = Path("resources/wyr_results/red_box.png")
            sent = self.ch1
        else:
            vote = self.votes2
            pat = Path("resources/wyr_results/blue_box_final.png")
            img_path = Path("resources/wyr_results/blue_box.png")
            sent = self.ch2

        rb_frame = Image.open(Path(f'{img_path}'))
        image_editabl = ImageDraw.Draw(rb_frame)
        h = rb_frame.height
        w = rb_frame.width
        margin = math.ceil(0.10*w)
        box_width = w-margin

        obj = FormWyr()
        arr = obj.form_sentences(
            sentence=sent, font=self.fontq, image_editable=image_editabl, boxwidth=box_width)
        arr += ['  ', '   ', f'{vote} votes']
        # making the y adjust based on number of sentences
        inline_spacing = 10
        y = (h/2)-len(arr)*(self.letter_height/2)

        for l in arr:
            text_width = image_editabl.textlength(l, font=self.fontq)
            # space to add to center the text in the box
            space = int((box_width-text_width)/2)
            x = space + math.ceil(margin/2)
            if l == arr[-1]:
                fontr = ImageFont.truetype(font=os.path.join(
                    'fonts', 'opensans_bold.ttf'), size= 48 if len(l)<75 else 42)
                image_editabl.text((x-25, y), text=l, font=fontr)
            else:
                image_editabl.text((x, y), text=l, font=self.fontq)
            y += self.letter_height + inline_spacing
            x = 0
        # rb_frame.show()
        rb_frame.save(Path(pat))
        return pat

    def form_result(self):
        frame = Image.open(Path("resources/wyr_results/frame.png"))
        image_editable = ImageDraw.Draw(frame)

        p1 = self.form_block(1)
        p2 = self.form_block(2)

        # making result bar
        fontw = ImageFont.truetype(font=os.path.join(
            'fonts', 'opensans_bold.ttf'), size=36)
        res = Image.open(Path("resources/wyr_results/result_bar.png"))
        result_bar_editable = ImageDraw.Draw(res)
        percentage1 = math.floor(
            (self.votes1/(1 if (self.votes1+self.votes2 == 0) else self.votes1+self.votes2))*100)
        percentage2 = (100-percentage1) if (self.votes1+self.votes2 != 0) else 0
        margin = 20
        hei = res.height
        wid = math.floor(res.width/2)-margin*2
        x1 = ((wid - result_bar_editable.textlength(str(percentage1), font=fontw))/2)+20
        print('x1 ,', x1)
        y = math.ceil(hei/2)-28
        result_bar_editable.text(
            (x1, y), text=str(f'{percentage1}%'), font=fontw)
        result_bar_editable.text(
            (x1+res.width/2-10, y), text=str(f'{percentage2}%'), font=fontw)
        res.save(Path("resources/wyr_results/result_bar_final.png"))
        Image.Image.paste(frame, Image.open(p1), (40, 34))
        Image.Image.paste(frame, Image.open(p2), (550, 34))
        Image.Image.paste(frame, Image.open(
            Path("resources/wyr_results/result_bar_final.png")), (209, 449))
        frame.save(Path("resources/wyr_results/result_wyr.png"))
        frame.show()

a=GetWyrResultImg('sfadf  ad  ad dasda','as dasd asd asdf',4545,122)
a.form_result()