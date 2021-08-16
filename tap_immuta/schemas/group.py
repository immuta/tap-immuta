from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.IntegerType),
    th.Property("iamid", th.StringType),
    th.Property("name", th.StringType),
    th.Property("gid", th.StringType),
    th.Property("email", th.StringType),
    th.Property("authorizations", th.ObjectType(
        th.Property("name", th.StringType),
    )),
    th.Property("description", th.StringType),
    th.Property("createdAt", th.StringType),
    th.Property("updatedAt", th.StringType),
).to_dict()
