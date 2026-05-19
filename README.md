data/data.csv is test data from the original task description



2.2 task benchmark with 5 mln rows

{'original': 107.57862901687622, 'pandas\_vectorised': 1.3321130275726318, 'polars': 1.483530044555664}



Original loop - 107s

Vectorized - 1.33s

Polars - 1.48



Original loop was slow, because it was processing data row by row

Vectorised pandas solution uses NumPy-based array operations , which are executed in compiled C code and therefore much faster (and in general Python is nbot very fast, in comparison, C is the fastest code language and python is almost 80 times slower)

Polars in theory should be even faster, but in my case it's a little bit slower. And it is probably because that not much manipulation is done with data, so vectorized pandas solution is more optimal for my case.



