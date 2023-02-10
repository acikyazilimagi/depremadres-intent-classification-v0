import pg_ops
import csv

conn = pg_ops.connect_to_db()

data = pg_ops.get_data(conn, 'tweets_depremaddress', ['id', 'full_text', 'tweet_id', 'geo_link'], '1=1')

# function to write data to csv file
def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(['id', 'full_text', 'tweet_id', 'geo_loc'])
        # writing the data rows
        csvwriter.writerows(data)

# write_to_csv(data, 'data.csv')