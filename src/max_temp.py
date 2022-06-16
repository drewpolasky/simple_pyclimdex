# All of the max temp related indices
# Assumes tmax will be given as a timerseries of daily maximum temperatures, starting january 1 without leap days
# returns values by year
# reference: https://www.climdex.org/learn/indices/

import numpy as np
import matplotlib.pyplot as plt


def tx_mean(tmax):
	"""
	annual mean max temperature
	:param tmax: array like
	:return:
	"""
	tmax = np.array(tmax)
	tmax_years = tmax.reshape(-1, 365)
	return np.nanmean(tmax_years, axis=1)


def su25(tmax, threshold=25):
	"""
	days above 25C, "summer days"
	:param tmax: array like
	:param threshold: optional, float, threshold above which to count number of days per year
	:return:
	"""
	tmax = np.array(tmax)
	tmax_years = tmax.reshape(-1, 365)
	return np.count_nonzero((tmax_years >= threshold), axis=1)


def id0(tmax, threshold=0):
	"""
	"icing days", max tmep below 0
	:param tmax: array like
	:param threshold: optional, float, threshold above which to count number of days per year
	:return:
	"""
	tmax = np.array(tmax)
	tmax_years = tmax.reshape(-1, 365)
	return np.count_nonzero((tmax_years <= threshold), axis=1)


def gsl(tmax, hemisphere='north', threshold=5, num_days=6):
	"""
	growing season length
	Annual count between the first span of at least 6 days with daily mean temperature TG >5 °C and the first span after
	July 1st (Jan 1st in SH) of 6 days with TG <5 °C.
	:param num_days:
	:param threshold:
	:param hemisphere:
	:param tmax:
	:return:
	"""
	tmax = np.array(tmax)
	tmax_years = tmax.reshape(-1, 365)
	season_lengths = []
	for i in range(tmax_years.shape[0]):
		season_start = None
		season_end = None
		span_above = 0
		span_below = 0
		for j in range(tmax_years.shape[1]):
			if tmax_years[i][j] >= threshold:
				span_above += 1
				span_below = 0
			else:
				span_below += 1
				span_above = 0
			if span_above == num_days and season_start is None:
				season_start = j - num_days + 1
			if span_below == num_days and season_end is None and season_start is not None:
				season_end = j - num_days + 1
		season_lengths.append(season_end - season_start)
	return season_lengths


def tx90p(tmax, threshold=None, reference_tmax=None):
	"""
	Days above the historical 90th percentile
	:param tmax:
	:param threshold: threshold value defining 90th percentile
	:param reference_tmax: Reference dataset to calculate 90th percentile from. If neither threshold nor reference_tmax
		are set, the threshold value will be calculated from tmax
	:return:
	"""
	tmax = np.array(tmax)
	tmax_years = tmax.reshape(-1, 365)

	if threshold is None:
		if reference_tmax is None:
			reference_tmax = tmax
		threshold = np.percentile(reference_tmax, 90)

	return np.count_nonzero((tmax_years >= threshold), axis=1)


def tx10p(tmax, threshold=None, reference_tmax=None):
	"""
		Days below the historical 10th percentile
		:param tmax:
		:param threshold: threshold value defining 90th percentile
		:param reference_tmax: Reference dataset to calculate 10th percentile from. If neither threshold nor reference_tmax
			are given, the threshold value will be calculated from tmax
		:return:
		"""
	tmax = np.array(tmax)
	tmax_years = tmax.reshape(-1, 365)

	if threshold is None:
		if reference_tmax is None:
			reference_tmax = tmax
		threshold = np.percentile(reference_tmax, 10)

	return np.count_nonzero((tmax_years <= threshold), axis=1)


def tx_max(tmax):
	"""
	annual max max temperature
	:param tmax: array like
	:return:
	"""
	tmax = np.array(tmax)
	tmax_years = tmax.reshape(-1, 365)
	return np.nanmax(tmax_years, axis=1)


def tx_min(tmax):
	"""
	annual min max temperature
	:param tmax: array like
	:return:
	"""
	tmax = np.array(tmax)
	tmax_years = tmax.reshape(-1, 365)
	return np.nanmin(tmax_years, axis=1)


def wsdi(tmax, threshold=None, reference_tmax=None, spell_duration=6):
	"""
	Warm spell duration index: annual count of days with at least 6 consecutive days when TX > 90th percentile
	:param spell_duration:
	:param tmax:
	:param threshold: threshold value defining 90th percentile
	:param reference_tmax: Reference dataset to calculate 10th percentile from. If neither threshold nor reference_tmax
		are given, the threshold value will be calculated from tmax
	:return:
	"""
	tmax = np.array(tmax)
	tmax_years = tmax.reshape(-1, 365)
	if threshold is None:
		if reference_tmax is None:
			reference_tmax = tmax
		threshold = np.percentile(reference_tmax, 90)

	years = []
	for i in range(tmax_years.shape[0]):
		span_above = 0
		num_days = 0
		for j in range(tmax_years.shape[1]):
			if tmax_years[i][j] >= threshold:
				span_above += 1
			else:
				if span_above > spell_duration:
					num_days += span_above
				span_above = 0
		years.append(num_days)
	return years


def dtr(tmax, tmin):
	pass


def test_indices():
	num_years = 10
	data = np.array([30 * np.sin(2 * (i - 90) / 365 * np.pi) for i in range(365 * num_years)]) + np.random.randint(-10,
			10, 365 * num_years)
	# plt.plot(data)
	# plt.show()

	func_list = [tx_mean, tx_min, tx_max, su25, id0, gsl, tx90p, tx10p, wsdi]
	for func in func_list:
		print(func.__name__)
		output = func(data)
		# plt.plot(output)
		# plt.title(str(func.__name__))
		print(output)
	# plt.show()


if __name__ == '__main__':
	test_indices()
