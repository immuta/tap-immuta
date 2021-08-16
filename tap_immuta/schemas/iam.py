from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("displayname", th.StringType),
    th.Property("type", th.StringType),
    th.Property("oauth", th.BooleanType),
).to_dict()
