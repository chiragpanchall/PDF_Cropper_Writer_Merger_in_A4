import sys
import os

from pdfrw import PdfReader, PdfWriter, PageMerge


def get4(srcpages):
    scale = 0.5
    srcpages = PageMerge() + srcpages
    x_increment, y_increment = (scale * i for i in srcpages.xobj_box[2:])
    for i, page in enumerate(srcpages):
        page.scale(scale)
        page.x = x_increment if i & 1 else 0
        page.y = 0 if i & 2 else y_increment
    return srcpages.render()


def getPDF(pdf):
    inpfn = pdf #sys.argv[1:]
    outfn = '4in1.' + os.path.basename(inpfn)
    pages = PdfReader(inpfn).pages
    writer = PdfWriter(outfn)
    for index in range(0, len(pages), 4):
        writer.addpage(get4(pages[index:index + 4]))
    writer.write()
