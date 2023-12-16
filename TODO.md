# Todo list
Don't hesitate to add coments and new todos

## Get nodes which include path
## Write First Fit algorithm
## Write Best Fit algorithm
## Have a good import structure. First public imports then imports from ours classes, functions 

## How get values of paths from proposed paths
My idea: \
We can create kind of function which will map it to us. \
We have 132 potential combination which works like following: 


> 0-1 -> 1 \
> 0-2 -> 2 \
> 0-3 -> 3 \
> 0-4 -> 4 \
> 0-5 -> 5 \
> 0-6 -> 6 \
> 0-7 -> 7 \
> 0-8 -> 8 \
> 0-9 -> 9 \
> 0-10 -> 10 \
> 0-11 -> 11 \
> 1-0 -> 12 \
> 1-2 -> 13 \
> 1-3 -> 14 \
> 1-4 -> 15 \
> 1-5 -> 16 \
> . \
> . \
> . 


So we can note schema for that. f(x, y) = x * 11 + y, \
where: 
> x -> input node \
> y -> output node \
> 11 -> max number of connections for one node in this network, generally it can be described as N-1, where N is number of nodes in graph.

When we have node_in = 1 and node_out = 5, so output will be 16.

When we have this number we can get all proposed paths stored in pol12.pat