import numpy as np
from scipy.optimize import minimize
from scipy.io import loadmat
from numpy.linalg import det, inv
from math import sqrt, pi
import scipy.io
import matplotlib.pyplot as plt
import pickle
import sys

def ldaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmat - A single d x d learnt covariance matrix 
    
    # IMPLEMENT THIS METHOD
    mu1=1
    mu2=1
    mu3=1
    mu4=1
    mu5=1
    c1=0;
    c2=0;
    c3=0;
    c4=0;
    c5=0;
    mean1 = 0
    mean2 = 0

    #print(y)
    for i in range(len(X)):
        if(y[i]==1):
            mu1 += X[i]
            c1+=1
            #print(mu1)
            #print(sum(X[i]))
        elif (y[i]==2):
            mu2 += (X[i])
            c2 += 1
            #print(mu2)
        elif (y[i]==3):
            mu3 += (X[i])
            c3 += 1
            #print(mu3)
        elif (y[i]==4):
            mu4 += (X[i])
            c4 += 1
            #print(mu4)
        elif (y[i]==5):
            mu5 += (X[i])
            c5 += 1
            #print(mu5, c5)


    mean1 += sum(X[:,0])
    mean2 += sum(X[:,1])

    mu1 /= c1;
    mu2 /= c2;
    mu3 /= c3;
    mu4 /= c4;
    mu5 /= c5;

    np.append([mu1], [mu2], axis=0)
    means = np.array([mu1, mu2, mu3, mu4, mu5])

    #print(mu1, mu2,mu3,mu4,mu5)
    means = means.transpose()
    #means=np.concatenate((mu1, mu2,mu3,mu4,mu5));
    #print(means)

    mean1 /= len(X);
    mean2 /= len(X);
    mean = np.array([mean1,mean2])
    #print("mu",mean)


    covmat = np.dot((X - mean).transpose(),(X-mean))* (1/len(X))
    #print(len(X))
    #mat = sum(np.power((X-mean), 2)) * (1/len(X))
    #print("Covmat",covmat)

    #covmat = np.array([[mat[0],0],[0,mat[1]]])

    #print(returnmeans)

    return means,covmat

def qdaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmats - A list of k d x d learnt covariance matrices for each of the k classes
    
    # IMPLEMENT THIS METHOD
    mu1=1
    mu2=1
    mu3=1
    mu4=1
    mu5=1
    c1=0;
    c2=0;
    c3=0;
    c4=0;
    c5=0;
    mean1 = 0
    mean2 = 0

    #print(y)
    for i in range(len(X)):
        if(y[i]==1):
            mu1 += X[i]
            c1+=1

        elif (y[i]==2):
            mu2 += (X[i])
            c2 += 1

        elif (y[i]==3):
            mu3 += (X[i])
            c3 += 1

        elif (y[i]==4):
            mu4 += (X[i])
            c4 += 1

        elif (y[i]==5):
            mu5 += (X[i])
            c5 += 1


    mean1 += sum(X[:,0])
    mean2 += sum(X[:,1])

    mu1 /= c1
    mu2 /= c2
    mu3 /= c3
    mu4 /= c4
    mu5 /= c5

    means = np.array([mu1, mu2, mu3, mu4, mu5])
    means = means.transpose()



    covmats=[]
    for i in range(len(np.unique(y))):

        select_indices = np.where(y==(i+1))[0]
        #print(X[select_indices])

        covmat = np.cov(X[select_indices].transpose())
        #print("cov",covmat)

        covmat = np.dot((X[select_indices] - means[:,i]).transpose(), (X[select_indices] - means[:,i])) * (1 / len(select_indices))
        #print("calculated", covmat)
        covmats.append(covmat)

    #print("mean",means)
    #print("cov",covmats)
    return means,covmats

def ldaTest(means,covmat,Xtest,ytest):
    # Inputs
    # means, covmat - parameters of the LDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    # ypred - N x 1 column vector indicating the predicted labels

    # IMPLEMENT THIS METHOD
    #np.exp(-1*(Xtest[]))

    list =[]

    for i in range(means.shape[1]):

        mat = np.dot((Xtest-means[:,i]), np.linalg.inv(covmat))
        #mat = np.dot(mat,(Xtest-means[:,i]).transpose())
        mat = mat * (Xtest - means[:, i])
        #result = np.power(np.linalg.det(covmat),(-1/2)) * np.exp((-1/2)*np.sum(mat,axis=1))
        result = np.exp((-1 / 2) * np.sum(mat, axis=1))
        list.append(result)


    ypred = np.array(list).transpose()
    ypred=ypred.argmax(1)+1
    #ypred = ypred.max(axis=1)
    ypred = np.reshape(ypred, (len(Xtest), 1))

    acc=np.sum(ypred==ytest)*(1/len(Xtest))
    acc=acc*100
    return acc,ypred

def qdaTest(means,covmats,Xtest,ytest):
    # Inputs
    # means, covmats - parameters of the QDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    # ypred - N x 1 column vector indicating the predicted labels

    # IMPLEMENT THIS METHOD
    list = []

    for i in range(means.shape[1]):
        mat = np.dot((Xtest - means[:, i]), np.linalg.inv(covmats[i]))
        #mat = np.dot(mat,(Xtest - means[:, i]).transpose())
        mat = mat * (Xtest - means[:, i])
        result = np.power(np.linalg.det(covmats[i]),(-1/2)) * np.exp( -1 * np.sum(mat, axis=1))
        #result =  np.exp(-1 * np.sum(mat, axis=1))
        list.append(result)

    #print(list)

    ypred = np.array(list).transpose()
    #print("Here",ypred)
    ypred = ypred.argmax(1) + 1
    #ypred=ypred.max(axis=1)
    #print("Here2",ypred)
    ypred = np.reshape(ypred, (len(Xtest), 1))
    #print(ypred)
    acc = np.sum(ypred == ytest) * (1/ len(Xtest))
    acc=acc*100
    return acc,ypred

def learnOLERegression(X,y):
    # Inputs:                                                         
    # X = N x d 
    # y = N x 1                                                               
    # Output: 
    # w = d x 1

    #w=np.dot(,)
    temp1=np.linalg.inv(np.dot(X.transpose(),X))
    temp2=np.dot(X.transpose(), y)

    w=np.dot(temp1, temp2)

    # IMPLEMENT THIS METHOD                                                   
    return w

def learnRidgeRegression(X,y,lambd):
    # Inputs:
    # X = N x d                                                               
    # y = N x 1 
    # lambd = ridge parameter (scalar)
    # Output:                                                                  
    # w = d x 1
    #print(X.shape, y.shape, lambd)
    temp1=np.linalg.inv(np.dot(X.transpose(),X)+(lambd * np.identity(len(X[0]))))
    temp2=np.dot(X.transpose(), y)

    w=np.dot(temp1, temp2)

    # IMPLEMENT THIS METHOD                                                   
    return w

def testOLERegression(w,Xtest,ytest):
    # Inputs:
    # w = d x 1
    # Xtest = N x d
    # ytest = X x 1
    # Output:
    # mse
    
    # IMPLEMENT THIS METHOD
    #print(ytest.shape, Xtest.shape, w.shape)
    mse=np.dot((ytest-np.dot(Xtest,w)).transpose(),(ytest-np.dot(Xtest,w))) * (1/len(ytest))

    return mse

def regressionObjVal(w, X, y, lambd):

    # compute squared error (scalar) and gradient of squared error with respect
    # to w (vector) for the given data X and y and the regularization parameter
    # lambda                                                                  

    # IMPLEMENT THIS METHOD

    w = np.reshape(w, (len(X[0]), 1))
    error=np.sum(np.dot((y - np.dot(X, w)).transpose(), (y - np.dot(X, w)))) + np.sum((1/2)*lambd*w)
    error_grad = (-1*np.dot(X.transpose(), (y-np.dot(X,w))) + 1*lambd * w ) * (1/len(X))

    error_grad=np.array(error_grad).flatten()
    error=np.array(error).flatten()

    return error, error_grad

def mapNonLinear(x,p):
    # Inputs:                                                                  
    # x - a single column vector (N x 1)                                       
    # p - integer (>= 0)                                                       
    # Outputs:                                                                 
    # Xd - (N x (d+1)) 
	
    # IMPLEMENT THIS METHOD


    x = np.reshape(x, (len(x), 1))
    Xd = np.zeros((len(x), (p+1)))
    if(p==0):
        res=1
    #print(Xd.shape)
    for i in range(len(x)):
        res = [x[i]**j for j in range(p+1)]
        #print(res)
        Xd[i]=res;

    #print(Xd.shape)
    return Xd

# Main script

# Problem 1
# load the sample data                                                                 
if sys.version_info.major == 2:
    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'))
else:
    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'),encoding = 'latin1')


# LDA
means,covmat = ldaLearn(X,y)
ldaacc,ldares = ldaTest(means,covmat,Xtest,ytest)
print('LDA Accuracy = '+str(ldaacc))
# QDA
means,covmats = qdaLearn(X,y)
qdaacc,qdares = qdaTest(means,covmats,Xtest,ytest)

print(qdares.shape)
print('QDA Accuracy = '+str(qdaacc))

# plotting boundaries
x1 = np.linspace(-5,20,100)
x2 = np.linspace(-5,20,100)
xx1,xx2 = np.meshgrid(x1,x2)
xx = np.zeros((x1.shape[0]*x2.shape[0],2))
xx[:,0] = xx1.ravel()
xx[:,1] = xx2.ravel()

fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)

zacc,zldares = ldaTest(means,covmat,xx,np.zeros((xx.shape[0],1)))
#print("Here333 LDA",np.unique(zldares))
#print("Here",zldares)
plt.contourf(x1,x2,zldares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)
plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest)
plt.title('LDA')

plt.subplot(1, 2, 2)

zacc,zqdares = qdaTest(means,covmats,xx,np.zeros((xx.shape[0],1)))
#print("Here333 QDA",np.unique(zldares))
plt.contourf(x1,x2,zqdares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)
plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest)
plt.title('QDA')

plt.show()
# Problem 2
if sys.version_info.major == 2:
    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'))
else:
    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'),encoding = 'latin1')

# add intercept
X_i = np.concatenate((np.ones((X.shape[0],1)), X), axis=1)
Xtest_i = np.concatenate((np.ones((Xtest.shape[0],1)), Xtest), axis=1)

w = learnOLERegression(X,y)
mle = testOLERegression(w,Xtest,ytest)
mle_train = testOLERegression(w,X,y)

w_i = learnOLERegression(X_i,y)
mle_i = testOLERegression(w_i,Xtest_i,ytest)
mle_i_train = testOLERegression(w_i,X_i,y)

print('Training MSE without intercept '+str(mle_train))
print('Training MSE with intercept '+str(mle_i_train))

print('Testing MSE without intercept '+str(mle))
print('Testing MSE with intercept '+str(mle_i))



# Problem 3
k = 101
lambdas = np.linspace(0, 1, num=k)
i = 0
mses3_train = np.zeros((k,1))
mses3 = np.zeros((k,1))
temp=99999999;
for lambd in lambdas:
    w_l = learnRidgeRegression(X_i,y,lambd)
    mses3_train[i] = testOLERegression(w_l,X_i,y)
    mses3[i] = testOLERegression(w_l,Xtest_i,ytest)
    if(temp>mses3[i]):
        temp=mses3[i]
        lambda_opt = lambd
        mse_opt = mses3[i]
        mse_opt_training = mses3_train[i]
    i = i + 1
print("Optimal Lambd = ",lambda_opt)
print("Optimal Training MSE = ",mse_opt_training)
print("Optimal Test MSE = ",mse_opt)
fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(lambdas,mses3_train)
plt.title('MSE for Train Data')
plt.subplot(1, 2, 2)
plt.plot(lambdas,mses3)
plt.title('MSE for Test Data')

plt.show()
# Problem 4
k = 101
lambdas = np.linspace(0, 1, num=k)
i = 0
temp11=9999999
temp12=9999999
mses4_train = np.zeros((k,1))
mses4 = np.zeros((k,1))
opts = {'maxiter' : 1000}    # Preferred value.
w_init = np.ones((X_i.shape[1],1))
for lambd in lambdas:
    args = (X_i, y, lambd)
    w_l = minimize(regressionObjVal, w_init, jac=True, args=args,method='CG', options=opts)
    w_l = np.transpose(np.array(w_l.x))
    w_l = np.reshape(w_l,[len(w_l),1])
    mses4_train[i] = testOLERegression(w_l,X_i,y)
    mses4[i] = testOLERegression(w_l,Xtest_i,ytest)
    if (temp11 > mses4_train[i]):
        temp11=mses4_train[i]
        #p11=p
    if (temp12 > mses4[i]):
        temp12=mses4[i]
        #p12=p
    i = i + 1
print("temp11 train",temp11)
print("temp12",temp12)

fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(lambdas,mses4_train)
plt.plot(lambdas,mses3_train)
plt.title('MSE for Train Data')
plt.legend(['Using scipy.minimize','Direct minimization'])

plt.subplot(1, 2, 2)
plt.plot(lambdas,mses4)
plt.plot(lambdas,mses3)
plt.title('MSE for Test Data')
plt.legend(['Using scipy.minimize','Direct minimization'])
plt.show()


# Problem 5
pmax = 7
#lambda_opt = 0.06 # REPLACE THIS WITH lambda_opt estimated from Problem 3
mses5_train = np.zeros((pmax,2))
mses5 = np.zeros((pmax,2))

mses5_train_zero = np.zeros((pmax,2))
mses5_zero = np.zeros((pmax,2))

lambda_zero=0
temp11=99999999
temp12=99999999
temp21=99999999
temp22=99999999




for p in range(pmax):
    Xd = mapNonLinear(X[:,2],p)
    Xdtest = mapNonLinear(Xtest[:,2],p)
    w_d1 = learnRidgeRegression(Xd,y,0)
    mses5_train[p,0] = testOLERegression(w_d1,Xd,y)
    mses5[p,0] = testOLERegression(w_d1,Xdtest,ytest)
    if(temp11 > mses5_train[p,0]):
        temp11=mses5_train[p,0]
        p11=p
    if (temp12 > mses5[p, 0]):
        temp12=mses5[p, 0]
        p12=p

    w_d2 = learnRidgeRegression(Xd,y,lambda_opt)
    mses5_train[p,1] = testOLERegression(w_d2,Xd,y)
    mses5[p,1] = testOLERegression(w_d2,Xdtest,ytest)
    if(temp21 > mses5_train[p,1]):
        temp21 =  mses5_train[p, 1]
        p21=p
    if (temp22 > mses5[p, 1]):
        temp22 = mses5[p, 1]
        p22=p

print("p11",p11)
print("p12",p12)
print("p21",p21)
print("p22",p22)

print("temp11",temp11)
print("temp12",temp12)
print("temp21",temp21)
print("temp22",temp22)

fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(range(pmax),mses5_train)
plt.title('MSE for Train Data using Lambda Optimal')
plt.legend(('No Regularization','Regularization'))
plt.subplot(1, 2, 2)
plt.plot(range(pmax),mses5)
plt.title('MSE for Test Data using Lambda Optimal')
plt.legend(('No Regularization','Regularization'))
plt.show()

