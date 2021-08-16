import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.cluster import KMeans

#from preface import prettyPrintTable

def prettyPrintTable(table, headers) :
    for i, d in enumerate(table):
        if i == 0 :
            line = '|'.join(str(x).ljust(30) for x in headers)
            print(line)
            print('-' * len(line))

        line = '|'.join(str(x).ljust(30) for x in d)
        print(line)
    print()

import boto3
import tempfile
s3 = boto3.resource('s3', region_name='us-east-1')
bucket = s3.Bucket('sss-compressr')
object = bucket.Object('shopping-street.jpg')
tmp = tempfile.NamedTemporaryFile()

with open(tmp.name, 'wb') as f:
    object.download_fileobj(f)
    img=mpimg.imread(tmp.name)
    #img = mpimg.imread('shopping-street.jpg')
    arr = np.array(img)
    chunks = np.zeros([13493,27])
    chunkPtr = 0
    
    # Transform dataset
    for i in range(0,arr.shape[0],3):
        for j in range(0,arr.shape[1],3):
            chunks[chunkPtr] = np.concatenate((arr[i,j], arr[i+1,j] ,arr[i+2,j],
                                 arr[i,j+1], arr[i+1,j+1], arr[i+2,j+1],
                                 arr[i,j+2], arr[i+1,j+2], arr[i+2,j+2]))
            chunkPtr = chunkPtr + 1

    imgplot = plt.imshow(arr)
    plt.get_current_fig_manager().set_window_title("Original")
    errors = []
    total_numbers = []
    compression_ratio = []

    for num_clusters in (2,5,10,25,50,100,200,1000):
        print("Current Num: ",num_clusters)
        kmeans = KMeans(n_clusters=num_clusters, init='random').fit(chunks)

        # Represent each 3x3 block with the centroid
        compressed_representation = kmeans.labels_

        # Reconstuct the image
        # Replace each pixel value with its nearby centroid
        compressed_image = kmeans.cluster_centers_[compressed_representation]
        compressed_image = np.clip(compressed_image.astype('uint8'), 0, 255)
        chunkPtr = 0

        # Reshape dimensions
        newImage = np.full(arr.shape,255)
        for i in range(0,arr.shape[0],3):
            for j in range(0,arr.shape[1],3):
                newImage[i,j] = compressed_image[chunkPtr][0:3]
                newImage[i+1,j] = compressed_image[chunkPtr][3:6]
                newImage[i+2,j] = compressed_image[chunkPtr][6:9]
                newImage[i,j+1] = compressed_image[chunkPtr][9:12]
                newImage[i+1,j+1] = compressed_image[chunkPtr][12:15]
                newImage[i+2,j+1] = compressed_image[chunkPtr][15:18]
                newImage[i,j+2] = compressed_image[chunkPtr][18:21]
                newImage[i+1,j+2] = compressed_image[chunkPtr][21:24]
                newImage[i+2,j+2] = compressed_image[chunkPtr][24:27]
                chunkPtr = chunkPtr + 1
    

    # Question 9
        imgplot = plt.imshow(newImage)
        plt.gca().set_axis_off()
        plt.get_current_fig_manager().set_window_title(f"k = {num_clusters}")
        plt.savefig(f"Compressed_image_with_num_clusters_{num_clusters}.jpg",bbox_inches='tight',pad_inches = 0)


    # Question 10
        diff = np.subtract(arr, newImage)
        diffSquared = np.square(diff)
        errors.append([int(num_clusters), np.mean(diffSquared)])


    # Question 11
        total_numbers.append([int(num_clusters), 27*num_clusters])

    # Question 12
        compression_ratio.append([int(num_clusters), (27*num_clusters/(arr.shape[0] * arr.shape[1] * arr.shape[2]))])

    print(f"\nReconstruction error :")
    prettyPrintTable(np.array(errors), ['Number of clusters','Reconstruction error'])  

    print(f"\nTotal numbers in reconstructed image :")
    prettyPrintTable(np.array(total_numbers), ['Number of clusters','Total numbers'])  

    print(f"\nCompression ratio :")
    prettyPrintTable(np.array(compression_ratio), ['Number of clusters','Compression ratio'])
