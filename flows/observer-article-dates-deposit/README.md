# observer-article-dates-deposit

The `observer-article-dates-deposit` flow requires no supporting scripts and does the transformations entirely within 
the flow itself using the built-in processors and a Jolt transformation (think JQ) to merge new content in.

The data is pulled from an elife project called 'Observer' that provides the RSS feeds to the journal but whose original
purpose was to create a denormalised database of article data for quickly generating reports in different 
serialisations. One of these reports is the `published-research-article-index` report that simply lists the article ID 
and two different types of publication date. 

The flow consumes this report from Observer once a day in it's JSON format and does a single atomic insert to BQ.
