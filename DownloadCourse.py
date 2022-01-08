import requests,os,json,wget,re
from bs4 import BeautifulSoup
from multiprocessing import Pool,Process
from tqdm import tqdm

if __name__ == "__main__":
    course_no = 'MATH1006'# input("请输入课程编号:\n")
    # url = 'https://video.cmet.ustc.edu.cn/college.html#/course/'+course_id
    # https://video.cmet.ustc.edu.cn/college.html#/course/top2019
    root_url = 'https://video.cmet.ustc.edu.cn'
    root_path = 'D:/课程相关及社团相关/B站运营/' # 自己安排路径
    # https://video.cmet.ustc.edu.cn/webservice/bizCoursesItem.action?userType=&no=top2019&reviewStatus=2&_=1641356329328
    course_url = 'https://video.cmet.ustc.edu.cn/webservice/bizCoursesItem.action?userType=&no='+str(course_no)
    videoCount = 20
    course_res = requests.get(course_url)
    if(course_res.status_code != 200):
        print('Error 1')
        exit()
    # print(course_res.text)
    # course_data['data']
    course_data = json.loads(course_res.text)
    course_name = course_data['data']['name']
    speaker = course_data['data']['speaker']
    if speaker != None:
        ddir = root_path+str(course_name)+' '+str(speaker)
    else:
        ddir = root_path+str(course_name)
    if(os.path.exists(ddir)==False):
        os.mkdir(ddir)
    remark = course_data['data']['remark']
    startTimeAndEndTimeTip = course_data['data']['startTimeAndEndTimeTip']
    videoCount = course_data['data']['videoCount']
    coures_cover_name = course_data['data']['coverHash']
    coures_cover_url = course_data['data']['coverUri']
    cdesc = "课程编号：%s\n课程名称：%s\n课程主讲：%s\n课程简介：%s\n起止时间：%s\n视频计数：%s\n"%(str(course_no), course_name, str(speaker), str(remark), startTimeAndEndTimeTip, str(videoCount))
    wget.download(root_url+coures_cover_url,ddir+'/'+coures_cover_name)
    with open(ddir+'/'+str(course_no)+'.txt','w',encoding='utf8') as df:
        df.write(cdesc)
    list_url =  'https://video.cmet.ustc.edu.cn/webservice/bizCoursesVideoList.action?parentCourses='+str(course_no)+'&parentVideoTitle=&PageIndex=1&PageSize='+str(max(videoCount,20))
    # https://video.cmet.ustc.edu.cn/webservice/bizCoursesVideoList.action?parentCourses=top2019&parentVideoTitle=&PageIndex=1&PageSize=20&reviewStatus=2&_=1641356329329
    list_res = requests.get(list_url)
    if(list_res.status_code != 200):
        print('Error 2')
        exit()
    # print(list_res.text)
    list_data = json.loads(list_res.text)
    print(list_data)
    download_title = []
    download_id = []
    download_cover_name = []
    download_cover_url = []
    download_desc = []
    for item_data in list_data['data']['list']:
        #print(item_data)
        video_cover_url = item_data['videoCoverUri']
        video_cover_name = item_data['videoCoverHash']
        videoId = item_data['videoId']
        item_data['sortNumber']
        
        
        videoTitle = item_data['videoTitle']
        download_title.append(videoTitle)
        download_id.append(str(videoId))
        download_cover_name.append(video_cover_name)
        download_cover_url.append(root_url+video_cover_url)
        desc = "课程编号：%s\n课程名称：%s\n视频序列：%s\n视频ID：%s\n视频标题：%s\n视频主讲：%s\n创建时间：%s\n视频时长：%s\n"%(item_data['coursesNo'], item_data['coursesName'], str(item_data['sortNumber']), str(videoId), videoTitle, str(item_data['videoSpeaker']), item_data['videoCreateTimeTip'], str(item_data['videoPeriodTip']))
        download_desc.append(desc)
    # i = 0
    for (dtitle,did,cname,curl,vdesc) in zip(download_title,download_id,download_cover_name,download_cover_url,download_desc):
        print(dtitle)
        dtitle_r=re.sub(r'[\\/:*?"<>|\r\n]+', "_", dtitle)
        dpath = ddir+'/'+str(dtitle_r)+'.mp4'
        durl = 'https://video.cmet.ustc.edu.cn/upload/video/'+str(did)+'/'+str(did)+'.mp4'
        # if i > 12:
        wget.download(durl,dpath)
        # i += 1
        wget.download(curl,ddir+'/'+cname)
        with open(ddir+'/'+did + ' ' + str(dtitle_r)+'.txt','w',encoding='utf8')as df:
            df.write(vdesc)

    print('下载完成!')
