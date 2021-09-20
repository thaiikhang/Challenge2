import cv2
import pandas as pd 
import glob
import numpy as np
import os.path

width = 800
height = 800
characs = ['A', 'B', 'C', 'D', 'E']

imglist = list()
studentlist = list()
fil = [os.path.basename(f) for f in glob.glob('Data/*.png')]
img_answer = cv2.imread('Answer/3A.png')#########


for name in fil:
    img = cv2.imread('Data/' + name)
    img = cv2.resize(img, (width, height))
    imglist.append(img)

    name = name.replace('.png','').split('_')
    student = [name[0], name[1], name[2]]
    studentlist.append(name)

#Question2
df_sheet_info = pd.DataFrame(studentlist, columns=['Student_ID','Name','Code'])
df_sheet_info.to_csv('student.csv')

def thresh_hold(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY_INV)
    return thresh

def crop_box_img(img,_box):
    ratio = [0,160,300,438,575,715,850]
    if 0 < _box < 7:
        img_crop = img[(ratio[_box]):(ratio[_box]+110),130:345]
        return img_crop
    elif 6 < _box < 13:
        img_crop = img[(ratio[_box-6]):(ratio[_box-6]+70),495:700] 
        return img_crop
    else:
        return img

def splitBoxes(image):
    rows = np.vsplit(image, 5)
    boxes = []
    for row in rows:
        cols = np.hsplit(row, 5)  
        for box in cols:  
            boxes.append(box)
    return boxes

def score_show(grading):
    score = (sum(grading)/60)*10
    score = "%.2f" % score
    return score

def pixelvalue(boxes):
    myPixelVal = np.zeros((5,5)) #question = 5, choice = 5
    countCol = 0
    countRow = 0
    for image in boxes:
        totalPixels = cv2.countNonZero(image)
        myPixelVal[countRow][countCol] = totalPixels
        countCol += 1
        if (countCol == 5):countRow += 1 ;countCol = 0
    return myPixelVal

def find_high_pixel(myPixelVal):    
    myIndex = list()
    for p in range (0,5):
        arr = myPixelVal[p]
        myIndexVal = np.where(arr==np.amax(arr))
        myIndex.append(myIndexVal[0][0])
    return myIndex

def grading(myIndex,ans):
    grade = []
    for g in range(0, 5):
        if ans[g] == myIndex[g]:
            grade.append(1)
        else:
            grade.append(0)
    return grade

def countscore(grade):
    score = (sum(grade)/60) * 10
    return score
x = 1

def _answer(i):
    ans = cv2.imread('Answer/3A.png')
    ans_key = []
    x = 1
    for x in range(0,14):
        _img = crop_box_img(ans,x)
        _thresh = thresh_hold(_img)
        _boxes = splitBoxes(_thresh)
        valuePixel = pixelvalue(_boxes)
        _index = find_high_pixel(valuePixel)
        x += 1
    return ans_key[i]

def _graded(imgIndex):
    int(imgIndex)
    graded = []
    x = 1
    for x in range(0,14):
        ansIndex = []
        _img = crop_box_img(imglist[imgIndex],x)
        _thresh = thresh_hold(_img)
        _boxes = splitBoxes(_thresh)
        valuePixel = pixelvalue(_boxes)
        _index = find_high_pixel(valuePixel)
        ansIndex.append(_index)
        ans_key = _answer(x - 1)
        _graded = grading(ansIndex[0],ans_key)
        graded.append(_graded)
        x += 1
    graded = np.concatenate(graded)
    score = score_show(graded)
    return score

def process_chars(index):
    char = []
    for x in range (0,5):
        for y in range (0,5):
            if index[x] == y:
                index[x] = characs[y]
    return index 

###Question 3
def Ques3():
    candi = cv2.imread('Data/2001002_Cao MyNhan_3A.png')
    char = []
    ansIndex = []
    _thresh = thresh_hold(crop_box_img(imglist[8],1))
    _boxes = splitBoxes(_thresh)
    valuePixel = pixelvalue(_boxes)
    _index = find_high_pixel(valuePixel)
    ansIndex.append(_index)
    char.append(process_chars(ansIndex[0]))
    print('The first 5 answer of CaoMyNhan')
    cv2.imshow('CaoMyNhan',candi)
    print(str(char))
Ques3()

def Ques4():
    char = []
    x = 1
    candi = cv2.imread('Data/2001002_Cao MyNhan_3A.png')
    while x < 13:
        char = []
        ansIndex = []
        _thresh = thresh_hold(crop_box_img(imglist[0],x))
        _boxes = splitBoxes(_thresh)
        valuePixel = pixelvalue(_boxes)
        _index = find_high_pixel(valuePixel)
        ansIndex.append(_index)
        char.append(process_chars(ansIndex[0]))
        x += 1
    chars = np.concatenate(char)
    print('All answers of the first student:')
    print(str(char))

#Ques4()
#Ques5
def correct_questions():
    all_score = list()
    for i in range (0,len(imglist)):     
        all_score.append(_graded(i))
    return all_score

def Ques5():
    correct = correct_questions()
    df_Score = pd.DataFrame({'Score':correct})
    df_ID = pd.DataFrame({'Student ID':df_sheet_info['Student ID']})
    frame = [df_ID,df_Score]
    grading = pd.concat(frame,axis=1)
    grading.to_csv('grading.csv')
Ques5()




cv2.waitKey()