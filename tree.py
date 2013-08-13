#__author__ = 'Arnold'
import sys,os
import urllib2,urllib,re
from datetime import datetime
from bs4 import BeautifulSoup, BeautifulStoneSoup
from ete2 import Tree, TreeStyle, NodeStyle, TextFace, faces, AttrFace
import mechanize
from HTMLParser import HTMLParser

username_list = []
email_list = []
manager_list = []

def cleanhtml(raw_html):
    cleanr =re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', raw_html)
    return cleantext

def toHex(dec):
    x = (dec % 16)
    digits = "0123456789ABCDEF"
    rest = dec / 16
    if (rest == 0):
        return digits[x]
    return toHex(rest) + digits[x]

def my_layout(node):
    if node.is_leaf():
        # If terminal node, draws its name
        name_faces = AttrFace("name")
    else:
        # If internal node, draws label with smaller font size
        name_faces = AttrFace("name", fsize=10)
    # Adds the name face to the image at the preferred position
    faces.add_face_to_node(name_faces, node, column=0, position="branch-right")

def isManager(name):
    if name in manager_list:
        return True
    else:
        return False


def getChildListOfManager(name):
    childlist = []
    for i in range(0, len(email_list)):
        if manager_list[i] == name:
            childlist.append(email_list[i])

    return childlist

def getTree(parentname, prefix, suffix):
    for child in getChildListOfManager(parentname):
        if isManager(child):
            if parentname != child:
                prefix = prefix + getTree(child, "(", ")" + child + "")
        else:
            prefix = prefix + "," + child + ","
    return prefix + suffix

def getRootName():
    for i in range(0, len(manager_list)):
        if manager_list[i] == '' or manager_list[i] == email_list[i]:
            rootname = email_list[i]
    return rootname

def addNodeCount(t, count):
    for child in t._children:
        if len(child._children) == 0:
            count = count + 1
        else:
            count = 1 + addNodeCount(child, 0)
    t.add_face(TextFace(str(count)), column=1, position = "branch-bottom")
    if (255 - count * 5) < 0:
        t.img_style["fgcolor"] = "#000000"
    else:
        t.img_style["fgcolor"] = "#00" + toHex(255 - count * 5) + "00"
    return count

def main(argv):

    print argv
    br = mechanize.Browser()
    directoryhtml = br.open(argv)
    t_soup = BeautifulSoup(directoryhtml.read())
    t_tables = t_soup.findAll('table',{"id":"people"})
    t_tbody = t_tables[0].findAll('tbody')
    t_trs = t_tbody[0].findAll('tr')
    for t_tr in t_trs:
        t_tds = t_tr.findAll('td')
        username = t_tds[0].find('a').find(text=True)
        email = t_tds[1].find('p').find(text=True)
        department = t_tds[2].find('p').find(text=True)
        title = t_tds[3].find('p').find(text=True)
        manager = t_tds[4].find('p').find(text=True)
        skypeid = t_tds[5].find('p').find(text=True)
        username_list.append(username)
        email_list.append(email[:email.find("@")])
        manager_list.append(manager)

    #Get the root manager
    rootname = getRootName()

    #Make the tree variable
    treeStr = getTree(rootname, "(", ")" + rootname + ";")
    treeStr = treeStr.replace("(,", "(")
    treeStr = treeStr.replace(",)", ")")
    treeStr = treeStr.replace(",,", ",")

    ts = TreeStyle()
    # Do not add leaf names automatically
    ts.show_leaf_name = False
    ts.show_branch_length = False
    ts.show_scale = False

    # Use my custom layout
    ts.layout_fn = my_layout

    t = Tree(treeStr, format=8)

    for n in t.traverse():
       nstyle = NodeStyle()
       nstyle["fgcolor"] = "red"
       nstyle["size"] = 15
       n.set_style(nstyle)

    count = 0
    addNodeCount(t, 0)
    #t.add_face(TextFace(str(addNodeCount(t, 0))), column=1, position = "branch-bottom")

    # Tell ETE to use your custom Tree Style
    t.show(tree_style=ts)
    t.render("tree_structure.png", w=183, units="mm")


if __name__ == "__main__":
#is being run directly
    main(sys.argv[1])
