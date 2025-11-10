from spctools_py.xmr import calculate_xmr

# test data, taken from Understanding SPC Dr. Donald Wheeler 3rd edition pg 386
#x is sixteen values in order from 1 to 16
x = list(range(1, 17))
y = [5045, 4350, 4350, 3975, 4290, 4430, 4485, 4285, 3980, 3925, 3645, 3760, 3300, 3685, 3463, 5200]
notes = "textbook data test of XmR function"

# run XmR calculation

result = calculate_xmr(x, y, notes)

print("Timestamp:", result.timestamp)
print("Notes:", result.notes)
print("Mean:", result.mean)
print("MRbar:", result.mr_bar)
print("UCL:", result.ucl)
print("LCL:", result.lcl)
print("URL:", result.url)
print("Warnings:", result.warnings)
print("Moving Ranges:", result.mr)