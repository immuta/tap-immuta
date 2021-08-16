from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("deleted", th.BooleanType),
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("source", th.StringType),
    th.Property("systemCreated", th.BooleanType),
).to_dict()
