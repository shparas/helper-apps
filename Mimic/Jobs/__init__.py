import glob

# put files with name job_*.py
# must have execute() function that accepts the raw text as action
# must return status, data, and misc as output

split = "/"
gl = glob.glob('Jobs/job_*')
if len(gl) > 0:
	if gl[0].find("\\") > 0:
		split = "\\"
	if gl[0].find("/") > 0:
		split = "/"
	jobs_raw = [x.split(split)[-1] for x in gl]
	jobs = [x.split(".py")[0] for x in jobs_raw]
	__all__ = jobs
