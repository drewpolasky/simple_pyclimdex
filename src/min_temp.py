# All of the min temp related indices
# Assumes tmin will be given as a timerseries of daily maximum temperatures, starting january 1 without leap days

import numpy as np


def tn_mean(tmin):
	"""
	annual mean min temperature
	:param tmin: array like
	:return:
	"""
	tmin = np.array(tmin)
	tmin_years = tmin.reshape(-1, 365)
	return np.nanmean(tmin_years, axis=1)


def tr20(tmin, threshold=20):
	"""
	nights below 20C, "opical nights"
	:param tmin: array like
	:param threshold: optional, float, threshold above which to count number of days per year
	:return:
	"""
	tmin = np.array(tmin)
	tmin_years = tmin.reshape(-1, 365)
	return np.count_nonzero((tmin_years <= threshold), axis=1)


def tn90p(tmin, threshold=None, reference_tmin=None):
	"""
	Days above the historical 90th percentile
	:param tmin:
	:param threshold: threshold value defining 90th percentile
	:param reference_tmin: Reference dataset to calculate 90th percentile from. If neither threshold nor reference_tmin
		are set, the threshold value will be calculated from tmin
	:return:
	"""
	tmin = np.array(tmin)
	tmin_years = tmin.reshape(-1, 365)

	if threshold is None:
		if reference_tmin is None:
			reference_tmin = tmin
		threshold = np.percentile(reference_tmin, 90)

	return np.count_nonzero((tmin_years >= threshold), axis=1)


def tn10p(tmin, threshold=None, reference_tmin=None):
	"""
		Days below the historical 10th percentile
		:param tmin:
		:param threshold: threshold value defining 90th percentile
		:param reference_tmin: Reference dataset to calculate 10th percentile from. If neither threshold nor reference_tmin
			are given, the threshold value will be calculated from tmin
		:return:
		"""
	tmin = np.array(tmin)
	tmin_years = tmin.reshape(-1, 365)

	if threshold is None:
		if reference_tmin is None:
			reference_tmin = tmin
		threshold = np.percentile(reference_tmin, 10)

	return np.count_nonzero((tmin_years <= threshold), axis=1)


def tn_max(tmin):
	"""
	annual max max temperature
	:param tmin: array like
	:return:
	"""
	tmin = np.array(tmin)
	tmin_years = tmin.reshape(-1, 365)
	return np.nanmax(tmin_years, axis=1)


def tn_min(tmin):
	"""
	annual min max temperature
	:param tmin: array like
	:return:
	"""
	tmin = np.array(tmin)
	tmin_years = tmin.reshape(-1, 365)
	return np.nanmin(tmin_years, axis=1)


def csdi(tmin, threshold=None, reference_tmin=None, spell_duration=6):
	"""
	Warm spell duration index: annual count of days with at least 6 consecutive days when TX > 90th percentile
	:param spell_duration:
	:param tmin:
	:param threshold: threshold value defining 10th percentile
	:param reference_tmin: Reference dataset to calculate 10th percentile from. If neither threshold nor reference_tmin
		are given, the threshold value will be calculated from tmin
	:return:
	"""
	tmin = np.array(tmin)
	tmin_years = tmin.reshape(-1, 365)
	if threshold is None:
		if reference_tmin is None:
			reference_tmin = tmin
		threshold = np.percentile(reference_tmin, 10)

	years = []
	for i in range(tmin_years.shape[0]):
		span_above = 0
		num_days = 0
		for j in range(tmin_years.shape[1]):
			if tmin_years[i][j] <= threshold:
				span_above += 1
			else:
				if span_above > spell_duration:
					num_days += span_above
				span_above = 0
		years.append(num_days)
	return years


def test_indices():
	num_years = 10
	data = np.array([30 * np.sin(2 * (i - 90) / 365 * np.pi) for i in range(365 * num_years)]) + np.random.randint(-10,
			10, 365 * num_years)
	# plt.plot(data)
	# plt.show()

	func_list = [tn_mean, tn_min, tn_max, tr20, tn90p, tn10p, csdi]
	for func in func_list:
		print(func.__name__)
		output = func(data)
		# plt.plot(output)
		# plt.title(str(func.__name__))
		print(output)
	# plt.show()


if __name__ == '__main__':
	test_indices()
