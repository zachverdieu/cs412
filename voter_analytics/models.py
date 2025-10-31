# File: voter_analytics/models.py
# Author: Zacharie Verdieu (zverdieu@bu.edu), 10/31/2025
# Description: FFile creating models for voter_analytics application

from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one voter in Massachusetts.
    '''

    # Voter Name
    last_name = models.TextField()
    first_name = models.TextField()
    
    # Residential Address Information
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.IntegerField()
    zip_code = models.CharField()

    # Important Dates
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    # Party + Precinct
    party_affiliation = models.CharField()
    precinct_number = models.IntegerField()

    # Election Participation
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()

    voter_score = models.IntegerField()

    def __str__(self):
        ''' returns a string representation of a Voter object'''

        return f'{self.first_name} {self.last_name}, member of the {self.party_affiliation} party, registered in {self.date_of_registration}, voter score: {self.voter_score}'

def load_data():
    '''Function to load data records from CSV file into the Django database.'''

    # very dangerous!
    Voter.objects.all().delete()

    filename = 'newton_voters.csv'
    f = open(filename, 'r') # open the file in readmode
    f.readline() # just skips first line of csv

    # This for loop attempts to store as much data from the csv as possible
    # adds records that do not cause any errors (empty fields, etc.)
    # displays an error message when an issue occurs
    for line in f:
        try:
            fields = line.strip().split(',')

            # defining a Voter object for current line in csv
            voter = Voter(
                last_name = fields[1],
                first_name = fields[2],
                
                street_number = fields[3],
                street_name = fields[4],
                apartment_number = fields[5],
                zip_code = fields[6],
                
                date_of_birth = fields[7],
                date_of_registration = fields[8],
                
                party_affiliation = fields[9],
                precinct_number = fields[10],

                v20state = fields[11],
                v21town = fields[12],
                v21primary = fields[13],
                v22general = fields[14],
                v23town = fields[15],
                voter_score = fields[16],
            )
            voter.save()

        except:
            print("Something went wrong!")
            print(f"line={line}")

    print(f"Created: {len(Voter.objects.all())} Results") # display added count