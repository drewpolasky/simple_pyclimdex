# All the prcp indices

import numpy as np
from itertools import groupby


def prcp_mean(prcp):
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)
	return np.nanmean(prcp_years, axis=1)


def rx1_day(prcp):
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)
	return np.nanmax(prcp_years, axis=1)


def rx5_day(prcp):
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)
	prcp_years = np.convolve(prcp_years, np.ones(5, type=int), 'valid')
	return np.nanmax(prcp_years, axis=1)


def r95p(prcp, threshold=95):
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)


def r99p(prcp):
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)


def sdii(prcp, threshold=0.01):
	"""
	simple precipitation intensity index -- precipitation on wet days
	:param threshold:
	:param prcp:
	:return:
	"""
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)
	sdii_years = prcp_years[prcp_years > threshold]
	sdii_values = np.mean(sdii_years, axis=1)
	return sdii_values


def cdd(prcp, thresh=0.1):
	"""
	longest spell of consecutive dry days per year
	:param prcp:
	:param thresh:
	:return:
	"""
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)
	cdd_values = []
	for i in range(prcp_years.shape[0]):
		cdd_values.append(
			max((sum(1 for _ in group) for value, group in groupby(prcp_years[i, :]) if value < thresh), default=0))
	return cdd_values


def cwd(prcp, thresh=0.1):
	"""
	longest spell of consecutive wet days per year
	:param prcp:
	:param thresh:
	:return:
	"""
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)
	cwd_values = []
	for i in range(prcp_years.shape[0]):
		cwd_values.append(
			max((sum(1 for _ in group) for value, group in groupby(prcp_years[i, :]) if value > thresh), default=0))
	return cwd_values


def r10mm(prcp, threshold=10):
	"""
	annual count of days with precipitation greater than threshold, default of 10mm
	:param threshold:
	:param prcp:
	:return:
	"""
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)
	r10_values = []
	for i in range(prcp_years.shape[0]):
		r10_values.append()

def r20mm(prcp):
	prcp = np.array(prcp)
	prcp_years = prcp.reshape(-1, 365)


if __name__ == '__main__':
	pass
