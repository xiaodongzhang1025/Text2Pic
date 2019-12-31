#coding:utf-8
__author__ = 'zhangxiaodong'
import sys
import os
import codecs
import time
import shutil
import codecs
import chardet
from PIL import Image,ImageDraw,ImageFont

reload(sys)
sys.setdefaultencoding('utf8')
    
def GetDataEncoding(data):
    data_encoding = None
    det_ret = chardet.detect(data)
    if det_ret:
        data_encoding = det_ret['encoding']
        #print det_ret
        #print 'data_encoding', data_encoding
    if data_encoding == 'windows-1251':
        data_encoding = 'gbk'
        #print '    windows-1251 ==> gbk'
    return data_encoding
    
def Text2Pic(text_file):
    
    ###################################################################
    #############for encode detect
    title_encoding = GetDataEncoding(text_file)
    text_file = text_file.decode(title_encoding)
    #text_file = text_file.decode('gbk')    ######### GBK !!!!
    ###################################################################
    pic_file, txt_ext = os.path.splitext(text_file)
    if txt_ext != '.txt':
        return False
        
    print '\n\n==================================', text_file
    title_text = os.path.split(pic_file)[-1]
    print 'title', title_text
    
    pic_file = pic_file + '.png'
    print '   ', text_file, "===>", pic_file
    
    #template_img = Image.new('RGB', (1080, 2160), (255, 255, 255))
    template_img = Image.open('template.png')
    total_width = template_img.width
    total_height = template_img.height
    print total_width, total_height
    new_img = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    new_img.paste(template_img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    #################################################################
    title_color = (255, 0, 0)
    normal_color = (0, 0, 0)
    title_font = ImageFont.truetype('simsun.ttc', total_width/15)
    normal_font = ImageFont.truetype('simsun.ttc', total_width/20)
    ################################################################
    normal_encoding = 'utf-8'
    with open(text_file, 'rb') as file_hd:
        raw_data = file_hd.read(4096)
        normal_encoding = GetDataEncoding(raw_data)
        print 'normal_encoding', normal_encoding
            
    with codecs.open(text_file, 'r', normal_encoding) as file_hd: 
        lines = file_hd.readlines()
        line_height = normal_font.getsize(title_text)[1]*1.5    #####行间距1.5倍
        
        max_width = 0
        line_num = len(lines)
        for i, line in enumerate(lines):
            normal_text = line.strip()
            tmp_width = (total_width - normal_font.getsize(normal_text)[0])/2
            if max_width < tmp_width:
                max_width = tmp_width
        
        normal_start_x = 0
        if total_width > max_width:
            #normal_start_x = (total_width - max_width)/2    ######居中显示
            normal_start_x = normal_font.getsize(u"缩进")[0]    ######左侧缩进2字符
        title_start_x = (total_width - title_font.getsize(title_text)[0])/2    ######水平居中显示
        
        max_height = title_font.getsize(title_text)[1]*2 + line_num*line_height
        title_start_y = 0
        if total_height > max_height:
            #title_start_y = title_font.getsize(title_text)[1]
            title_start_y = (total_height - max_height)/2    ######垂直居中显示
        normal_start_y = title_start_y + title_font.getsize(title_text)[1]*2    
        draw.text((title_start_x, title_start_y), title_text, title_color, font=title_font)
        
        for i, line in enumerate(lines):
            normal_text = line.strip()
            print '    [%d]'%i, normal_text
            cure_pos_y = normal_start_y + line_height*i
            draw.text((normal_start_x, cure_pos_y), normal_text, normal_color, font=normal_font)
            
    new_img.show()
    print 'Start to save img...'
    new_img.save(pic_file)
    template_img.close()
    return True
    
if "__main__" == __name__:
    print '\n------------------------------The Start-----------------------------'
    target = os.getcwd()
    if len(sys.argv) >= 2:
        target = sys.argv[1]
    start_time = time.clock()
    
    #####################################################
    try:
        if os.path.isfile(target):
            print 'File', target
            Text2Pic(target)
        else:
            print 'Dir', target
            for root, dirs, files in os.walk(target):
                #print root, dirs, files
                for file in files:
                    #print file
                    Text2Pic(os.path.join(root, file))
    except Exception, err:
        #print err
        print '===> Exception'
        print str(err).decode("string_escape")
    finally:
        #print '===> Finally'
        print ''
    #####################################################
    print '------------------------------The   End-----------------------------'
    end_time = time.clock()
    print 'Time used %s senconds'%(end_time - start_time)
    sys.exit(0)