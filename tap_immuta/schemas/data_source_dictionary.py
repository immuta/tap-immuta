from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("dataSource", th.IntegerType),
    th.Property("types", th.ArrayType(th.StringType)),
    th.Property("id", th.IntegerType),
    th.Property("createdAt", th.StringType),
    th.Property("updatedAt", th.StringType),
    th.Property("metadata", th.ArrayType(
        th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("dataType", th.StringType),
            th.Property("nullable", th.BooleanType),
            th.Property("remoteType", th.StringType),
            th.Property("tags", th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("source", th.StringType),
                    th.Property("deleted", th.BooleanType),
                )),
            ),
        )),
    ),
).to_dict()
