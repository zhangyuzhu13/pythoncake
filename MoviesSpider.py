#coding:utf-8
'''
Created on 2016.9.9
@author: dell
'''
from bs4  import BeautifulSoup
import requests
from idlelib.IOBinding import encoding
import xlrd

def get_web_data(url):
    
    #get web content
    
    web_data = requests.get(url)
    return web_data

def get_all_tages(url):
    
    #get all tags and its relative url and return file
    
    web_data = get_web_data(url)
    Soup = BeautifulSoup(web_data.text,'lxml')
    
    tag_f = open("tags.txt",'a+')
    tags = Soup.select('#app > div > div.tags-panel > ul > li:nth-of-type(1) > ul > li  > a')
      
    for tag in tags:
        tag_f.write("%s\n"%tag.get_text())
        tag_f.write("%s\n"%tag.get('href'))
    tag_f.close()
    return tag_f

def get_all_movie_of_a_type(type_url,type):
    
    web_data = get_web_data(type_url)
    Soup = BeautifulSoup(web_data.text,'lxml')
    
    movies_f = open("%s.txt"%type,"a+")
    
    movies = Soup.select('div.channel-detail.movie-item-title > a')
     
    for movie   in   movies  :
        movies_f.write('%s\n'%movie.get_text())
        movies_f.write('%s\n'%movie.get('href'))
    movies_f.close()
    

def get_all_comments_of_a_movie(movie_url,movie):
    
    web_data = get_web_data(movie_url)
    Soup = BeautifulSoup(web_data.text,'lxml')
    comments_f = open('%s.txt'%movie,'a+',encoding='utf-8')
    comments = Soup.select(' div.comment-content')
   
    for comment in comments:
        
        comments_f.write(comment.get_text())
    comments_f.close()
    
def spider(url):
    #excute the crawl steps
    get_all_tages(url)
    data = xlrd.open_workbook('comment.xls')
    table = data.sheets()[0]
    
    f = open('tags.txt','r')
    
    temp = 0
    for line in f:
        temp = temp + 1
        
        if not line:
            break
        elif temp < 3:
            continue
        elif temp%2==1:
            type = line.strip('\n')
            
        else:
             
            type_url = 'http://maoyan.com/films'+line
            get_all_movie_of_a_type(type_url, type)
            ff = open("%s.txt"%type,'r')
            inside_temp = 0
            for inside_line in ff:
                inside_temp = inside_temp + 1
                if not inside_line:
                    break
                elif inside_temp%2==1:
                    
                    movie = inside_line.strip('\n')
                else:
                     
                    movie_url = 'http://maoyan.com'+inside_line.strip('\n')
                    
                    get_all_comments_of_a_movie(movie_url,movie)
                
            ff.close()
    f.close()
        
    
    
    
if  __name__ == "__main__":
    url = "http://maoyan.com/films?"
    #web_data = get_web_data(url)
    #get_all_tages(web_data)
    #type_url = "http://maoyan.com/films?catId=3"
    #get_all_movie_of_a_type(type_url)
    #movie_url = 'http://maoyan.com/films/247575'
    #get_all_comments_of_a_movie(movie_url, '不二情书') 
    spider(url)
    
    print('finish')
    