import sys
sys.path.append('/home/sean/boarders/boarders/')
DJANGO_SETTINGS_MODULE = "settings.py"
import glob
import os
from boardermash.models import Boarder

def get_info(filename):
    fh = open(filename)
    av_link = ""
    av_src = ""
    av_height = 200
    av_width = 200
    dname = ""
    location = ""
    num_posts = ""
    next_span_user = False
    next_img_av = False
    next_dd_posts = False
    for l in fh:
	if l.find("<dl class=\"left-box\">") > 0:
	    next_img_av = True
	if l.find("<img src=") > 0 and next_img_av == True:
	    av_link = "<" + l.strip().lstrip("<dt>").rstrip("</dt>").strip() + ">"
	    next_img_av = False
	if l.find("<dt>Username:</dt>") > 0:
	    next_span_user = True
	if l.find("span") > 0 and next_span_user == True:
	    dname =  l.strip()
	    next_span_user = False
	    next_img_av = False
	if l.find("<dt>Location:</dt>") > 0:
	    start = l.find("<dd>")
	    stop = l.find("</dd>")
	    location = l[start+4:stop]
	if l.find("<dt>Total posts:</dt>") > 0:
	    next_dd_posts = True
	if l.find("<dd>") > 0 and next_dd_posts == True:
	    num_posts = l.split("|")[0].strip().lstrip("<dd>").strip()
	    next_dd_posts = False	

    if av_link.find("src=\"") > 0:
	    src_start = av_link.find("src=\"") + 5
	    src_stop = av_link.find("\"", src_start)
	    av_src = av_link[src_start:src_stop]
	    if av_src.find("./download") == 0:
		av_src = "http://forums.hipinion.com" + av_src.lstrip(".")
    if av_link.find("height=\""):
	    ht_start = av_link.find("height=\"") + 8
	    ht_stop = av_link.find("\"", ht_start)
	    if av_link[ht_start:ht_stop] <> "":
		av_height = int(av_link[ht_start:ht_stop]) 
    if av_link.find("width=\""):
	    wd_start = av_link.find("width=\"") + 7
	    wd_stop = av_link.find("\"", wd_start)
	    if av_link[wd_start:wd_stop] <> "":
		av_width = int(av_link[wd_start:wd_stop]) 
    return {"av_link":av_src, "av_height":av_height, "av_width":av_width, "dname":dname, "location":location, "num_posts":num_posts}

def import_boarders():
    blist = glob.glob("boarder_files/*")
    for b in blist:
	fname = os.path.split(b)[1]
	info = get_info(b)
	dname = info['dname']
	num_posts = int(info['num_posts'])
	avatar_link = info['av_link']
	avatar_height = info['av_height']
	avatar_width = info['av_width']
	location = info['location']
	score = 1400
	newb = Boarder(fname=fname, dname=dname, num_posts=num_posts, avatar_link=avatar_link, avatar_height=avatar_height, avatar_width=avatar_width, location=location, score=score)
	newb.save()

if __name__=='__main__':
    import_boarders()
