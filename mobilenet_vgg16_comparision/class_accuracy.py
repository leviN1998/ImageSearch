import mobilenet_extractor as extractor
import os
import re 
from statistics import mean

'''
tests class accuracy of mobilenet and vgg16
'''

#checks if given string is equal to one of the classes or not
def isClass(name):
    classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    return True if(name in classes) else False

#retrieves classname (or name of img) of a given img_path
def getClassName(path):
    basename = os.path.basename(path)
    classname = os.path.splitext(basename)[0]
    temp = re.compile("([a-zA-Z]+)([0-9]+)")
    classname = temp.match(classname).groups()[0]
    return classname

'''
calculates top5, top10 and top15 accuracy of prediction for ONE image
requires result set with at least 16 similar images
img_paths must be like this: ../../class01.jpg

gives back array with topX percentages of shape like this:
[top5, top10, top15]
'''

def getPredictionAccuracy(query_img_path, feature_dir):
    
    query_img_class = getClassName(query_img_path)
        
    query_feature = extractor.extractImage(query_img_path)
    results = extractor.compareImages(query_feature, feature_dir)[1:] #cut off first element, as this will be the query img itself
    print('results: ')
    print(results)
    print("\n")
    
    #percentage of how many of the results have the same class as query img
    c= 0; top5 = 0; top10 = 0

    for i in range(len(results)):
                
        result_class = getClassName(results[i][1]) 
        if( result_class == query_img_class ):
            c = c+1

        if( i == 4):
            top5 = (c / 5)
        if( i == 9):
            top10 = (c / 10) #'{:.2%}'.format

    return [top5, top10, (c / len(results))]



'''
calculates top5, top10, top15 class accuracy for all images/features in a directory
returns mean value and single values (=results)
'''
def totalClassAccuracy(img_dir, feature_dir):
    results = []
    means = []
    images = os.listdir(img_dir)

    for i in range(len(images)):
        result = getPredictionAccuracy(img_dir + '/' + images[i], feature_dir)
        #print('result of ' + str(i) + 'image: \n' )
        #print(result)
        results.append(result)

    # calculate mean values of topX
    for j in range(3):
        means[j] = mean(results[i][j] for i in range(len(results)))

    return results, means

if __name__=="__main__":
    img_dir = './static/images'
    m_feature_dir = './static/m_features'

    #query_img_path = './static/images/automobile34.jpg'
    
    #res = test(query_img_path, feature_dir)
    #print(res)

    results, means = totalClassAccuracy(img_dir, m_feature_dir)
    print('results: ')
    print(results)
    print('\n')
    print('means: ')
    print(means)