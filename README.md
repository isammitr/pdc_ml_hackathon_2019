# PDC Hackathon

[![version][version-badge]][CHANGELOG]


# Installation
1. Clone this repo. 
2. Run these commands in Administrator command prompt

        set PYTHONIOENCODING=utf8
        
        pip install -r requirements.txt
        
# Description

Hi,

we have find that there is a pattern in the data so we created a feature vector using below parameters from json data.

feature vector:

X_data :

	category prediction

	[ petition_petition_status,_source_sponsored_campaign, _source_sponsorship_active, petition_primary_target_is_person, petition_sponsored_campaign, petition_organization_non_profit ]

Y_data : 

	[petition_is_victory]

prediction :

	petition_category
	petition_is_victory 



# Testing

1.  Run below commands for testing above ml engine.

```
# command to initiate run the training process.
python train.py 

# ommand to initiate run the scoring process.
python score.py -f "validation/validation.json"

python score.py --filepath "validation/validation.json"

```
[CHANGELOG]: ./CHANGELOG.md
[version-badge]: https://img.shields.io/badge/version-0.0.0-green.svg

