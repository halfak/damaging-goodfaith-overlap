
datasets/enwiki.revision_sample.nonbot_10k.json:
	wget https://quarry.wmflabs.org/run/173476/output/0/json-lines?download=true -qO- > \
	datasets/enwiki.revision_sample.nonbot_10k.json

datasets/enwiki.scored_revision_sample.nonbot_10k.json:
	cat datasets/enwiki.revision_sample.nonbot_10k.json | \
	python score_revisions.py \
	  https://ores.wikimedia.org enwiki damaging goodfaith > \
	datasets/enwiki.scored_revision_sample.nonbot_10k.json

datasets/enwiki.scored_revision_sample.nonbot_10k.tsv:
	cat datasets/enwiki.scored_revision_sample.nonbot_10k.json | \
	grep -v error | \
	json2tsv \
	  rev_id \
	  score.damaging.score.probability.true \
	  score.goodfaith.score.probability.true \
	  --header > \
	datasets/enwiki.scored_revision_sample.nonbot_10k.tsv
