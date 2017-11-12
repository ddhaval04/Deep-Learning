import numpy as np
from random import shuffle

def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.
  Inputs:
  - W: K x D array of weights
  - X: D x N array of data. Data are D-dimensional columns
  - y: 1-dimensional array of length N with labels 0...K-1, for K classes
  - reg: (float) regularization strength
  Returns:
  a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero
  delta = 1 # margin of the SVM
  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  scores = W.dot(X)
  yi_scores = scores[y, np.arange(0, scores.shape[1])]
  margins = np.maximum(0, scores - np.matrix(yi_scores) + delta)
  margins[y, np.arange(X.shape[1])] = 0
  loss = np.mean(np.sum(margins, axis = 1))
  loss += 0.5 * reg * np.sum(W * W)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################

  intermediate = margins
  intermediate[intermediate > 0] = 1
  intermediate[y, np.arange(0, scores.shape[1])] = 0
  intermediate[y, np.arange(0, scores.shape[1])] = -np.sum(intermediate, axis=0)
  dW = np.dot(intermediate, X.T)

  # Average over number of training examples
  num_train = X.shape[1]
  dW /= num_train
  dW += reg*W
  
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
