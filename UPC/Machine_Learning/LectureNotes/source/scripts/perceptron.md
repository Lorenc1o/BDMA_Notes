# Perceptron Example

```matlab:Code
rng(5)
X = rand([100,1]);
y = 2*(double(X>0.5)-0.5*ones(size(X)));

f=gscatter(X,zeros(size(X)),y,'br','o');
hold on
ylim([-0.1,0.1])
hold off
```

![/home/jose/Desktop/Lorenc1o-repos/BDMA_Notes/UPC/Machine_Learning/LectureNotes/source/scripts/perceptron_images/figure_0.png
](perceptron_images//home/jose/Desktop/Lorenc1o-repos/BDMA_Notes/UPC/Machine_Learning/LectureNotes/source/scripts/perceptron_images/figure_0.png
)

  

Now, let's manually use our perceptron:

```matlab:Code
W = [-0.5; 1]
```

```text:Output
W = 2x1    
   -0.5000
    1.0000

```

```matlab:Code

% Add the bias
X_bias = [ones(size(X)) X];

pred = zeros(size(X));

for i=1:length(X)
    x = X_bias(i,:)';
    S = state(x,W);
    pred(i) = my_sign(S);
end

f2=gscatter(X,zeros(size(X)),pred,'br','o');
hold on
ylim([-0.1,0.1])
hold off
```

![/home/jose/Desktop/Lorenc1o-repos/BDMA_Notes/UPC/Machine_Learning/LectureNotes/source/scripts/perceptron_images/figure_1.png
](perceptron_images//home/jose/Desktop/Lorenc1o-repos/BDMA_Notes/UPC/Machine_Learning/LectureNotes/source/scripts/perceptron_images/figure_1.png
)

It classified perfectly! Now let's train the algorithm:

```matlab:Code
% Add the bias
X_bias = [ones(size(X)) X];

% Train the model
W2 = train(X_bias,y,0.1,10)
```

```text:Output
W2 = 2x1    
   -0.1000
    0.2013

```

```matlab:Code

pred2 = zeros(size(X_bias));

for i=1:length(X)
    x = X_bias(i,:)';
    S = state(x,W2);
    pred2(i) = my_sign(S);
end

f3=gscatter(X,zeros(size(X)),pred2,'br','o');
hold on
ylim([-0.1,0.1])
hold off
```

![/home/jose/Desktop/Lorenc1o-repos/BDMA_Notes/UPC/Machine_Learning/LectureNotes/source/scripts/perceptron_images/figure_2.png
](perceptron_images//home/jose/Desktop/Lorenc1o-repos/BDMA_Notes/UPC/Machine_Learning/LectureNotes/source/scripts/perceptron_images/figure_2.png
)

This is quite interesting... it found different weights, but it classified eveything well. This must break somewhere. Let's try to determine where:

```matlab:Code
X = 0.45:0.001:0.55;
X = X';
y = 2*(double(X>0.5)-0.5*ones(size(X)));

X_bias = [ones(size(X)) X];

pred3 = zeros(size(X));

for i=1:length(X)
    x = X_bias(i,:)';
    S = state(x,W2);
    pred3(i) = my_sign(S);
end

f4=gscatter(X_bias,zeros(size(X)),pred3==y,'br','o');
hold on
ylim([-0.1,0.1])
xlim([0.45,0.55])
hold off
```

![/home/jose/Desktop/Lorenc1o-repos/BDMA_Notes/UPC/Machine_Learning/LectureNotes/source/scripts/perceptron_images/figure_3.png
](perceptron_images//home/jose/Desktop/Lorenc1o-repos/BDMA_Notes/UPC/Machine_Learning/LectureNotes/source/scripts/perceptron_images/figure_3.png
)

```matlab:Code

y(pred3~=y)
```

```text:Output
ans = 4x1    
    -1
    -1
    -1
    -1

```

This means that our model is actually setting the bound a little bit before 0.5 (as can be seen in the graph). This should be improved by increasing the size of X.

```matlab:Code
function S = state(X, W)
    S = W'*X;
end

function pred = my_sign(S)
    if S > 0
        pred = 1;
    else
        pred = -1;
    end
end

function W = train(X, y, lr, epochs)
    [~, d] = size(X);
    W = zeros(d, 1);
    for epoch = 1:epochs
        for i = 1:length(X)
            x = X(i,:)';
            pred = my_sign(state(x, W));
            if pred ~= y(i)
                W = W + lr*x*y(i);
            end
        end
    end
end

```
