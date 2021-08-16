from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("dateTime", th.StringType),
    th.Property("dataSourceName", th.StringType),
    th.Property("projectName", th.StringType),
    th.Property("recordType", th.StringType),
    th.Property("blobId", th.StringType),
    th.Property("userId", th.StringType),
    th.Property("profileId", th.IntegerType),
    th.Property("purposeIds", th.ArrayType(th.StringType)),
    th.Property("success", th.BooleanType),
    th.Property("failureReason", th.StringType),
    th.Property("id", th.StringType),
    th.Property("fingerprintVersionName", th.StringType),
    th.Property("email", th.StringType),
).to_dict()
