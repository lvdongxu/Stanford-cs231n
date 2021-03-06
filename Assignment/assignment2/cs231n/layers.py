from builtins import range
import numpy as np


def affine_forward(x, w, b):
    """
    Computes the forward pass for an affine (fully-connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    ###########################################################################
    # TODO: Implement the affine forward pass. Store the result in out. You   #
    # will need to reshape the input into rows.                               #
    ###########################################################################
    
    N = x.shape[0]
    x_reshape = x.reshape([N, -1])
    out = x_reshape.dot(w) + b
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """
    Computes the backward pass for an affine layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the affine backward pass.                               #
    ###########################################################################
    N = x.shape[0]
    x_reshape = x.reshape([N, -1]) #首先需要将乘积项中的x的维度给调整好，不然没法乘
    dx = dout.dot(w.T).reshape(*x.shape) #后面这个reshape的意思是将dx按照x的shape来构建
    dw = (x_reshape.T).dot(dout)
    db = np.sum(dout, axis=0) #不管是按照那个维度加起来，加起来之后的维度都是集中在axis=0
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Implement the ReLU forward pass.                                  #
    ###########################################################################
    out = np.maximum(0, x)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Implement the ReLU backward pass.                                 #
    ###########################################################################
    dx = dout * (x >= 0)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def batchnorm_forward(x, gamma, beta, bn_param):
    """
    Forward pass for batch normalization.

    During training the sample mean and (uncorrected) sample variance are
    computed from minibatch statistics and used to normalize the incoming data.
    During training we also keep an exponentially decaying running mean of the
    mean and variance of each feature, and these averages are used to normalize
    data at test-time.

    At each timestep we update the running averages for mean and variance using
    an exponential decay based on the momentum parameter:

    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggests a different test-time
    behavior: they compute sample mean and variance for each feature using a
    large number of training images rather than using a running average. For
    this implementation we have chosen to use running averages instead since
    they do not require an additional estimation step; the torch7
    implementation of batch normalization also uses running averages.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    mode = bn_param['mode']
    eps = bn_param.get('eps', 1e-5)
    momentum = bn_param.get('momentum', 0.9)

    N, D = x.shape
    running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
    running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

    out, cache = None, None
    if mode == 'train':
        #######################################################################
        # TODO: Implement the training-time forward pass for batch norm.      #
        # Use minibatch statistics to compute the mean and variance, use      #
        # these statistics to normalize the incoming data, and scale and      #
        # shift the normalized data using gamma and beta.                     #
        #                                                                     #
        # You should store the output in the variable out. Any intermediates  #
        # that you need for the backward pass should be stored in the cache   #
        # variable.                                                           #
        #                                                                     #
        # You should also use your computed sample mean and variance together #
        # with the momentum variable to update the running mean and running   #
        # variance, storing your result in the running_mean and running_var   #
        # variables.                                                          #
        #######################################################################
        
        sample_mean = np.mean(x, axis=0)
        sample_var = np.var(x, axis=0)
        x_norm = (x - sample_mean) / (np.sqrt(sample_var + eps)) # 归一化
        out = gamma * x_norm + beta # 新的out

        cache = (gamma, x, sample_mean, sample_var, eps, x_norm)
        running_mean = momentum * running_mean + (1 - momentum) * sample_mean
        running_var = momentum * running_var + (1 - momentum) * sample_var 

        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test-time forward pass for batch normalization. #
        # Use the running mean and variance to normalize the incoming data,   #
        # then scale and shift the normalized data using gamma and beta.      #
        # Store the result in the out variable.                               #
        #######################################################################
        
        # test时候的标准化需要用到 gamma/beta 还有计算出来的 running_mean/var
        scale = gamma / np.sqrt(running_var + eps)
        out = x * scale + beta - running_mean * scale
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

    # Store the updated running means back into bn_param
    bn_param['running_mean'] = running_mean
    bn_param['running_var'] = running_var

    return out, cache


def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from batchnorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    ###########################################################################
    n = dout.shape[0]
    gamma, x, mean, var, eps, x_norm = cache 
    # 按照公式顺序一步步推
    # 第一个公式：loss对x_norm的偏导数
    dx_norm = dout * gamma
    # 第二个公式：loss对var的偏导数
    dvar = np.sum(dx_norm * (x - mean) * (-0.5) * (var + eps) ** (-1.5), axis=0)
    # 第三个公式：loss对mean的偏导数
    dmean = np.sum(dx_norm, axis=0) * (-1) / np.sqrt(var + eps) + dvar * np.sum(-2 * (x - mean), axis=0) / n
    # 第四个公式：loss对x的偏导数，前三个公式的集合
    dx = dx_norm / np.sqrt(var + eps) + dvar * 2 * (x - mean) / n + dmean / n
    # 第五个公式：loss对gamma的偏导数
    dgamma = np.sum(dout * x_norm, axis=0)
    # 第六个公式：loss对beta的偏导数
    dbeta = np.sum(dout, axis=0)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
    """
    Alternative backward pass for batch normalization.

    For this implementation you should work out the derivatives for the batch
    normalizaton backward pass on paper and simplify as much as possible. You
    should be able to derive a simple expression for the backward pass.

    Note: This implementation should expect to receive the same cache variable
    as batchnorm_backward, but might not use all of the values in the cache.

    Inputs / outputs: Same as batchnorm_backward
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    #                                                                         #
    # After computing the gradient with respect to the centered inputs, you   #
    # should be able to compute gradients with respect to the inputs in a     #
    # single statement; our implementation fits on a single 80-character line.#
    ###########################################################################
    
    # 参考网站为：http://cthorey.github.io/backpropagation/，虽然没有看懂为啥
    n = dout.shape[0]
    gamma, x, mean, var, eps, x_norm = cache 
    # gamma：loss对gamma的偏导数
    dgamma = np.sum(dout * x_norm, axis=0)
    # beta：loss对beta的偏导数
    dbeta = np.sum(dout, axis=0)
    # x: loss对x的偏导数
    dx = (1. / n) * gamma * (var + eps)**(-1. / 2.) * (n * dout - np.sum(dout, axis=0) - (x - mean) * (var + eps)**(-1.0) * np.sum(dout * (x - mean), axis=0))
    
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
    """
    Performs the forward pass for (inverted) dropout.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
      - p: Dropout parameter. We drop each neuron output with probability p.
      - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
      - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not
        in real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: tuple (dropout_param, mask). In training mode, mask is the dropout
      mask that was used to multiply the input; in test mode, mask is None.
    """
    p, mode = dropout_param['p'], dropout_param['mode']
    if 'seed' in dropout_param:
        np.random.seed(dropout_param['seed'])

    mask = None
    out = None

    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase forward pass for inverted dropout.   #
        # Store the dropout mask in the mask variable.                        #
        #######################################################################
        
        # 不知道为什么教程都这样写，我很奇怪，不过其实和小于是一样的
        mask = (np.random.rand(*x.shape) >= p) / (1 - p)
        out = x * mask

        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test phase forward pass for inverted dropout.   #
        #######################################################################
        
        out = x

        #######################################################################
        #                            END OF YOUR CODE                         #
        #######################################################################

    cache = (dropout_param, mask)
    out = out.astype(x.dtype, copy=False)

    return out, cache


def dropout_backward(dout, cache):
    """
    Perform the backward pass for (inverted) dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask = cache
    mode = dropout_param['mode']

    dx = None
    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase backward pass for inverted dropout   #
        #######################################################################
        dx = dout * mask
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    elif mode == 'test':
        dx = dout
    return dx


def conv_forward_naive(x, w, b, conv_param):
    """
    A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width HH.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    # N：样本数，C：通道数，H：高度，W：宽度
    N, C, H, W = x.shape
    # F：卷积核个数，C：通道数，HH：高度，WW：宽度
    F, _, HH, WW = w.shape
    # 步长
    stride = conv_param['stride']
    # padding
    pad = conv_param['pad']
    # 卷积之后输出的维度计算
    x_pad = np.pad(x, ((0,), (0,), (pad,), (pad,)), 'constant')
    out_h = 1 + (H + 2 * pad - HH) // stride
    out_w = 1 + (W + 2 * pad - WW) // stride
    out = np.zeros([N, F, out_h, out_w])

    for j in range(out_h):
        for k in range(out_w):
            h_coord = min(j * stride, H + 2 * pad - HH)
            w_coord = min(k * stride, W + 2 * pad - WW)
            for i in range(F):
                out[:, i, j, k] = np.sum(x_pad[:, :, h_coord:h_coord+HH, w_coord:w_coord+WW] * w[i, :, :, :], axis=(1, 2, 3))
    out = out + b[None, :, None, None]
    
    '''
    for n in range(N):
          for f in range(F):
                conv_out = np.ones([out_H, out_W]) * b[f]
                for c in range(C):
                      x_pad = np.lib.pad(x[n, c], pad_width=pad, mode='constant', constant_values=0)
                      for h in range(out_H):
                            for w in range(out_W):
                                  conv_out[h, w] += np.sum(x_pad[h*stride : h*stride+HH, w*stride : w*stride+WW] * w[f, c, :, :], axis=(1,2,3))
                out[n, f] = conv_out 
    '''  
    '''
    # pad
    x_pad = np.pad(x, ((0, 0), (0, 0), (pad, pad),(pad, pad)), 'constant')
    # 计算
    for n in range(N): # N个样本
        for f in range(F): # F个卷积核
            for h in range(out_H): # 高度遍历
                for w in range(out_W): # 宽度遍历
                    out[n, f, h, w] = np.sum(x_pad[n, :, h*stride : (h*stride+HH), w*stride : (w*stride+WW)] * w[f,:,:,:], axis=(1,2,3)) + b[f] # 卷积运算的矩阵表示
    '''
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b, conv_param)
    return out, cache


def conv_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a convolutional layer.

    Inputs:
    - dout: Upstream derivatives.
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    '''
    # 数据准备
    x, w, b, conv_param = cache
    pad = conv_param['pad']
    stride = conv_param['stride']
    F, C, HH, WW = w.shape
    N, C, H, W = x.shape
    N, F, new_H, new_W = dout.shape

    # 下面，我们模拟卷积，首先填充x。
    padded_x = np.lib.pad(x,
                          ((0, 0), (0, 0), (pad, pad), (pad, pad)),
                          mode='constant',
                          constant_values=0)
    padded_dx = np.zeros_like(padded_x)  # 填充了的dx，后面去填充即可得到dx
    dw = np.zeros_like(w)
    db = np.zeros_like(b)
    
    for n in range(N):  # 第n个图像
        for f in range(F):  # 第f个过滤器
            for i in range(new_H):
                for j in range(new_W):
                    #dw 等于所有out的每一个像素求导之和，因为out每个像素都共享参数
                    db[f] += dout[n, f, i, j] # dg对db求导为1*dout
                    dw[f] += padded_x[n, :, i*stride : HH + i*stride, j*stride : WW + j*stride] * dout[n, f, i, j]
                    padded_dx[n, :, i*stride : HH + i*stride, j*stride : WW + j*stride] += w[f] * dout[n, f, i, j]
    # 去掉填充部分
    dx = padded_dx[:, :, pad:pad + H, pad:pad + W]
    '''
    '''
    # Grab conv parameters and pad x if needed.
    x, w, b, conv_param = cache
    stride = conv_param.get('stride')
    pad = conv_param.get('pad')
    padded_x = (np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)), 'constant'))

    N, C, H, W = x.shape
    F, C, HH, WW = w.shape
    N, F, H_out, W_out = dout.shape

    # Initialise gradient output tensors.
    dx_temp = np.zeros_like(padded_x)
    dw = np.zeros_like(w)
    db = np.zeros_like(b)

    # Calculate dB.
    # Just like in the affine layer we sum up all the incoming gradients for each filters bias.
    for ff in range(F):
        db[ff] += np.sum(dout[:, ff, :, :])

    # Calculate dw.
    # By chain rule dw is dout*x
    for nn in range(N):
        for ff in range(F):
            for jj in range(H_out):
                for ii in range(W_out):
                    dw[ff, ...] += dout[nn, ff, jj, ii] * padded_x[nn,:,jj*stride:jj*stride+HH,ii*stride:ii*stride+WW]

    # Calculate dx.
    # By chain rule dx is dout*w. We need to make dx same shape as padded x for the gradient calculation.
    for nn in range(N):
        for ff in range(F):
            for jj in range(H_out):
                for ii in range(W_out):
                    dx_temp[nn, :, jj*stride:jj*stride+HH,ii*stride:ii*stride+WW] += dout[nn, ff, jj,ii] * w[ff, ...]

    # Remove the padding from dx so it matches the shape of x.
    dx = dx_temp[:, :, pad:H+pad, pad:W+pad]
    '''
    
    # 各种尺寸信息的计算
    x, w, b, conv_param = cache
    stride, pad = conv_param['stride'], conv_param['pad']
    N, C, H, W = x.shape
    F, C, HH, WW = w.shape
    N, F, out_H, out_W = dout.shape
    # out_H = 1 + int((H - HH + 2*pad) / stride)
    # out_W = 1 + int((W - WW + 2*pad) / stride)
    # out = np.zeros([N, F, out_H, out_W])
    # 构建梯度的矩阵
    x_pad = np.lib.pad(x, ((0,0),(0,0),(pad,pad),(pad,pad)), mode='constant', constant_values=0)
    dx_pad = np.zeros_like(x_pad)
    dw = np.zeros_like(w)
    db = np.zeros_like(b)
    # 按照循环一步步计算
    for nn in range(N):
          for ff in range(F):
                for i in range(out_H):
                      for j in range(out_W):
                            db[ff] += dout[nn, ff, i, j] # db就是dout的累加，与DNN的是一样的
                            dw[ff] += x_pad[nn, :, i*stride:i*stride+HH, j*stride:j*stride+WW] * dout[nn, ff, i, j] # dw其实也应该与DNN是一样，dout*x
                            dx_pad[nn, :, i*stride:i*stride+HH, j*stride:j*stride+WW] += dout[nn, ff, i, j] * w[ff]
    dx = dx_pad[:, :, pad:pad+H, pad:pad+W]
    
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def max_pool_forward_naive(x, pool_param):
    """
    A naive implementation of the forward pass for a max pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
      - 'pool_height': The height of each pooling region
      - 'pool_width': The width of each pooling region
      - 'stride': The distance between adjacent pooling regions

    Returns a tuple of:
    - out: Output data
    - cache: (x, pool_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the max pooling forward pass                            #
    ###########################################################################
    # 先确定形状
    N, C, H, W = x.shape
    # 确定池化的参数
    pool_height, pool_width, stride = pool_param['pool_height'], pool_param['pool_width'], pool_param['stride']
    # 计算维度
    out_H = 1 + (H - pool_height) // stride
    out_W = 1 + (W - pool_width) // stride
    out = np.zeros([N, C, out_H, out_W])
    # 循环计算
    for nn in range(N):
        for cc in range(C):
            for hh in range(out_H):
                for ww in range(out_W):
                    out[nn, cc, hh, ww] = np.max(x[nn, cc, hh*stride:hh*stride+pool_height, ww*stride:ww*stride+pool_width])
    
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, pool_param)
    return out, cache


def max_pool_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a max pooling layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x
    """
    dx = None
    ###########################################################################
    # TODO: Implement the max pooling backward pass                           #
    ###########################################################################
    # 基本参数的获得
    x, pool_param = cache
    pool_height, pool_width, stride = pool_param['pool_height'], pool_param['pool_width'], pool_param['stride']
    # 矩阵维度的确定
    N, C, H, W = x.shape
    _, _, out_H, out_W = dout.shape
    dx = np.zeros_like(x)
    # 循环计算
    for nn in range(N):
        for cc in range(C):
            for hh in range(out_H):
                for ww in range(out_W):
                    window = x[nn, cc, hh*stride:hh*stride+pool_height, ww*stride:ww*stride+pool_width]
                    m = np.max(window)
                    dx[nn, cc, hh*stride:hh*stride+pool_height, ww*stride:ww*stride+pool_width] = (window == m) * dout[nn, cc, hh, ww]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
    """
    Computes the forward pass for spatial batch normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance. momentum=0 means that
        old information is discarded completely at every time step, while
        momentum=1 means that new information is never incorporated. The
        default of momentum=0.9 should work well in most situations.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None

    ###########################################################################
    # TODO: Implement the forward pass for spatial batch normalization.       #
    #                                                                         #
    # HINT: You can implement spatial batch normalization using the vanilla   #
    # version of batch normalization defined above. Your implementation should#
    # be very short; ours is less than five lines.                            #
    ###########################################################################
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return out, cache


def spatial_batchnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial batch normalization.      #
    #                                                                         #
    # HINT: You can implement spatial batch normalization using the vanilla   #
    # version of batch normalization defined above. Your implementation should#
    # be very short; ours is less than five lines.                            #
    ###########################################################################
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def svm_loss(x, y):
    """
    Computes the loss and gradient using for multiclass SVM classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    N = x.shape[0]
    correct_class_scores = x[np.arange(N), y]
    margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
    margins[np.arange(N), y] = 0
    loss = np.sum(margins) / N
    num_pos = np.sum(margins > 0, axis=1)
    dx = np.zeros_like(x)
    dx[margins > 0] = 1
    dx[np.arange(N), y] -= num_pos
    dx /= N
    return loss, dx


def softmax_loss(x, y):
    """
    Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    shifted_logits = x - np.max(x, axis=1, keepdims=True)
    Z = np.sum(np.exp(shifted_logits), axis=1, keepdims=True)
    log_probs = shifted_logits - np.log(Z)
    probs = np.exp(log_probs)
    N = x.shape[0]
    loss = -np.sum(log_probs[np.arange(N), y]) / N
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    return loss, dx
