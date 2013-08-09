#__author__ = 'Arnold'
import sys,os
import urllib2,urllib,re
from datetime import datetime
from bs4 import BeautifulSoup
from ete2 import Tree, TreeStyle, NodeStyle, TextFace
import mechanize

def main(argv):
    print argv
    br = mechanize.Browser()
    directoryhtml = br.open(argv)
    t_soup = BeautifulSoup(directoryhtml.read())


    t = Tree( "(a,b);" )

    # Basic tree style
    ts = TreeStyle()
    ts.show_leaf_name = True

    # Creates two faces
    hola = TextFace("hola")
    mundo = TextFace("mundo")

    # Set some attributes
    hola.margin_top = 10
    hola.margin_right = 10
    hola.margin_left = 10
    hola.margin_bottom = 10
    hola.opacity = 0.5 # from 0 to 1
    hola.inner_border.width = 1 # 1 pixel border
    hola.inner_border.type = 1  # dashed line
    hola.border.width = 1
    hola.background.color = "LightGreen"

    t.add_face(hola, column=0, position = "branch-top")
    t.add_face(mundo, column=1, position = "branch-bottom")

    t.show(tree_style=ts)
    #t.render("mytree.png", w=183, units="mm")


if __name__ == "__main__":
#is being run directly
    main(sys.argv[1])
