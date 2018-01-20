# https://stats.stackexchange.com/questions/121107/is-there-a-name-or-reference-in-a-published-journal-book-for-the-following-varia
# https://stats.stackexchange.com/questions/55999/is-it-possible-to-find-the-combined-standard-deviation

# TODO: Cite some text book.
# TODO: Average absolute deviation vs standard deviation.

from math import sqrt

from itertools import imap # Lazy map.

def unpack_tuple(f):
  """Return a unary function that calls `f` with its argument unpacked."""
  return lambda args: f(*iter(args))

class sampled_value(object):
  """A list of observed values.

  Attributes:
    quantity (scalar)               : The quantity of the value.
    variance (scalar)               : The variance of the value. 
    samples  (`int`)                : The number of observations in the value.
    unit     (unit class or `None`) : The units the value is measured in.
  """

  def __init__(self, quantity, variance, samples = 1, unit = None):
    self.quantity    = quantity
    self.variance = variance
    self.samples     = samples
    self.unit        = unit

  def __iter__(self):
    return iter((self.quantity, self.variance, self.samples, self.unit))

def arithmetic_mean(X):
  """Computes the arithmetic mean of the sequence `X`.

  Let:

    * `n = len(X)`.
    * `u` denote the arithmetic mean of `X`.

  .. math::

    u = \frac{\sum_{i = 0}^{n - 1} X_i}{n}
  """
  return sum(X) / len(X)

def sample_variance(X, u = None):
  """Computes the sample variance of the sequence `X`.

  Let:

    * `n = len(X)`.
    * `u` denote the arithmetic mean of `X`.
    * `s` denote the sample standard deviation of `X`.

  .. math::

    v = \frac{\sum_{i = 0}^{n - 1} (X_i - u)^2}{n - 1}

  Args:
    X (`Iterable`) : The sequence of values.
    u (number)     : The arithmetic mean of `X`.
  """
  if u is None: u = arithmetic_mean(X)
  return sum(imap(lambda X_i: (X_i - u) ** 2, X)) / (len(X) - 1)
 
def sample_standard_deviation(X, u = None, v = None):
  """Computes the sample standard deviation of the sequence `X`.

  Let:

    * `n = len(X)`.
    * `u` denote the arithmetic mean of `X`.
    * `v` denote the sample variance of `X`.
    * `s` denote the sample standard deviation of `X`.

  .. math::

    s &= \sqrt{v}
      &= \sqrt{\frac{\sum_{i = 0}^{n - 1} (X_i - u)^2}{n - 1}}

  Args:
    X (`Iterable`) : The sequence of values.
    u (number)     : The arithmetic mean of `X`.
    v (number)     : The sample variance of `X`.
  """
  if u is None: u = arithmetic_mean(X)
  if v is None: v = sample_variance(X, u)
  return sqrt(v)

def combined_sample_size(As):
  """Computes the combined sample variance of a group of `sampled_value`s.

  Let:

    * `g = len(As)`.
    * `n_i = As[i].samples`.
    * `n` denote the combined sample size of `As`.

  .. math::

    n = \sum{i = 0}^{g - 1} n_i
  """
  return sum(imap(unpack_tuple(lambda u_i, v_i, n_i, t_i: n_i), As))

def combined_arithmetic_mean(As, n = None):
  """Computes the combined arithmetic mean of a group of `sampled_value`s.

  Let:

    * `g = len(As)`.
    * `u_i = As[i].quantity`.
    * `n_i = As[i].samples`.
    * `n` denote the combined sample size of `As`.
    * `u` denote the arithmetic mean of the quantities of `As`.

  .. math::

    u = \frac{\sum{i = 0}^{g - 1} n_i u_i}{n}
  """
  if n is None: n = combined_sample_size(As)
  return sum(imap(unpack_tuple(lambda u_i, v_i, n_i, t_i: n_i * u_i), As)) / n
  
def combined_sample_variance(As, n = None, u = None):
  """Computes the combined sample variance of a group of `sampled_value`s.

  Let:

    * `g = len(As)`.
    * `u_i = As[i].quantity`.
    * `v_i = As[i].variance`.
    * `n_i = As[i].samples`.
    * `n` denote the combined sample size of `As`.
    * `u` denote the arithmetic mean of the quantities of `As`.

  .. math::

    v = \frac{(\sum_{i = 0}^{g - 1} n_i (u_i - u)^2 + v_i (n_i - 1))}{n - 1}

  Args:
    As (`Iterable` of `sampled_values`) : The sequence of values.
    n (number)                          : The combined sample sizes of `As`.
    u (number)                          : The combined arithmetic mean of `As`.
  """
  if n is None: n = combined_sample_size(As)
  if u is None: u = combined_arithmetic_mean(As, n)
  return sum(imap(unpack_tuple(
    lambda u_i, v_i, n_i, t_i: n_i * (u_i - u) ** 2 + v_i * (n_i - 1)
  ), As)) / (n - 1)

def combined_sample_standard_deviation(As, n = None, u = None, v = None):
  """Computes the combined sample standard deviation of a group of `sampled_value`s.

  Let:

    * `g = len(As)`.
    * `u_i = As[i].quantity`.
    * `v_i = As[i].variance`.
    * `n_i = As[i].samples`.
    * `n` denote the combined sample size of `As`.
    * `u` denote the arithmetic mean of the quantities of `As`.
    * `v` denote the sample variance of `X`.
    * `s` denote the sample standard deviation of `X`.

  .. math::

    s &= \sqrt{v}
      &= \sqrt{\frac{(\sum_{i = 0}^{g - 1} n_i (u_i - u)^2 + v_i (n_i - 1))}{n - 1}}

  Args:
    As (`Iterable` of `sampled_values`) : The sequence of values.
    n (number)                          : The combined sample sizes of `As`.
    u (number)                          : The combined arithmetic mean of `As`.
    v (number)                          : The combined sample variance of `As`.
  """
  if n is None: n = combined_sample_size(As)
  if u is None: u = combined_arithmetic_mean(As, n)
  if v is None: v = combined_sample_variance(As, n, u)
  return sqrt(v)

###############################################################################
# Testing
###############################################################################

def numpy_sample_standard_deviation(X):
  from numpy import std   as numpy_std
  from numpy import array as numpy_array
  return numpy_std(numpy_array([X]), ddof = 1)

a = [3.7, 4.5, 4.3, 4.7, 4.6, 3.4, 4.1, 3.3]
b = [3.6, 4.1, 4.0, 4.1, 4.4]
c = [4.4, 3.9, 4.2, 4.1, 4.5, 3.8, 4.0, 4.3]
d = [4.0, 3.9, 4.1]

print "our amean of a:  ", arithmetic_mean(a)
print "our amean of b:  ", arithmetic_mean(b)
print "our amean of c:  ", arithmetic_mean(c)
print "our amean of d:  ", arithmetic_mean(d)

print "numpy sstdev of a:", numpy_sample_standard_deviation(a)
print "numpy sstdev of b:", numpy_sample_standard_deviation(b)
print "numpy sstdev of c:", numpy_sample_standard_deviation(c)
print "numpy sstdev of d:", numpy_sample_standard_deviation(d)

print "our sstdev of a:  ", sample_standard_deviation(a)
print "our sstdev of b:  ", sample_standard_deviation(b)
print "our sstdev of c:  ", sample_standard_deviation(c)
print "our sstdev of d:  ", sample_standard_deviation(d)

print "numpy sstdev of a + b:", numpy_sample_standard_deviation(a + b)
a_sv = sampled_value(arithmetic_mean(a), sample_variance(a), len(a))
b_sv = sampled_value(arithmetic_mean(b), sample_variance(b), len(b))
print "our amean of a + b:   ", arithmetic_mean(a + b)
print "our sstdev of a + b:  ", sample_standard_deviation(a + b)
print "our camean of a + b:  ", combined_arithmetic_mean([a_sv, b_sv])
print "our csstdev of a + b: ", combined_sample_standard_deviation([a_sv, b_sv])

print "numpy sstdev of a + b + c:", numpy_sample_standard_deviation(a + b + c)
a_sv = sampled_value(arithmetic_mean(a), sample_variance(a), len(a))
b_sv = sampled_value(arithmetic_mean(b), sample_variance(b), len(b))
c_sv = sampled_value(arithmetic_mean(c), sample_variance(c), len(c))
print "our amean of a + b + c:   ", arithmetic_mean(a + b + c)
print "our sstdev of a + b + c:  ", sample_standard_deviation(a + b + c)
print "our camean of a + b + c:  ", combined_arithmetic_mean([a_sv, b_sv, c_sv])
print "our csstdev of a + b + c: ", combined_sample_standard_deviation([a_sv, b_sv, c_sv])


