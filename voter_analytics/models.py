from django.db import models

# Create your models here.

class Voter(models.Model):
    """ class to define each Newton voter model """
    # identification
    first_name = models.TextField()
    last_name = models.TextField()
    street_num = models.IntegerField()
    street_name = models.TextField()
    apt_num = models.TextField(blank=True)
    zip_code = models.IntegerField()
    dob = models.DateField()

    # voting information
    registration_date = models.DateField()
    party = models.CharField(max_length=1)
    precinct_num = models.CharField(max_length=2)

    # election participation
    v20state = models.CharField(max_length=5)
    v21town = models.CharField(max_length=5)
    v21primary = models.CharField(max_length=5)
    v22general = models.CharField(max_length=5)
    v23town = models.CharField(max_length=5)
    voter_score = models.IntegerField()
    def __str__(self):
        return f'{self.first_name} {self.last_name} DOB: {self.dob}, Address: {self.street_num} {self.street_name}'

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    filename = 'newton_voters.csv'
    f = open(filename)
    headers = f.readline() # discard headers

    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()
    
    # go through entire file 
    for line in f:
        fields = line.split(',')
        try:
            voter = Voter(last_name = fields[1].strip(),
                          first_name = fields[2].strip(),
                          street_num = fields[3].strip(),
                          street_name = fields[4].strip(),
                          apt_num = fields[5],
                          zip_code = fields[6],
                          dob = fields[7],

                          registration_date = fields[8],
                          party = fields[9].strip(),
                          precinct_num = fields[10],

                          v20state = fields[11],
                          v21town = fields[12],
                          v21primary = fields[13],
                          v22general = fields[14],
                          v23town = fields[15],
                          voter_score = fields[16],
                          )
            voter.save()
            print(f'Created voter: {voter}')
        except:
            print(f'Skipped: {voter}')

    print("Done")
