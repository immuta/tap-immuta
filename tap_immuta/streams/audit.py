import singer

from tap_immuta.streams.base import BaseStream
from tap_immuta.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class AuditStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'audit'
    KEY_PROPERTIES = ['id']
    RESPONSE_RESULT_KEY = "hits"

    IS_SELECTED_BY_DEFAULT = False

    CACHE_RESULTS = False

    RECORD_TYPES = [
        'blobVisibility',
        'blobFetch',
        'blobIndex',
        'blobDelete',
        'blobUpdateFeatures',
        'blobUpdateTags',
        'sqlAccess',
        'spark',
        'sqlCreateUser',
        'sqlDeleteUser',
        'sqlResetPassword',
        'featureList',
        'sqlQuery',
        'dataSourceCreate',
        'dataSourceDelete',
        'dataSourceExpired',
        'dataSourceSave',
        'dataSourceGet',
        'dataSourceListMine',
        'dataSourceSubscription',
        'dictionaryCreate',
        'dictionaryDelete',
        'dictionaryUpdate',
        'projectCreate',
        'projectUpdate',
        'projectDelete',
        'addToProject',
        'removeFromProject',
        'projectSubscription',
        'acknowledgePurposes',
        'accessUser',
        'accessGroup',
        'apiKey',
        'tagAdded',
        'tagCreated',
        'tagDeleted',
        'tagUpdated',
        'tagRemoved',
        'authenticate',
        'checkPendingRequest',
        'policyExemption',
        'governanceUpdate',
        'purposeCreate',
        'purposeUpdate',
        'purposeDelete',
        'licenseCreate',
        'licenseDelete',
        'policyHandlerCreate',
        'policyHandlerUpdate',
        'globalPolicyCertify',
        'globalPolicyCreate',
        'globalPolicyUpdate',
        'globalPolicyDelete',
        'globalPolicyConflictResolved',
        'globalPolicyDisabled',
        'globalPolicyApplied',
        'globalPolicyRemoved',
        'hdfsUserChanged',
        'externalQuery',
        'fingerprintVersionCreate',
        'fingerprintVersionUpdate',
        'fingerprintVersionDelete',
        'unmaskRequest',
        'queryDebugRequest',
        'taskDelete',
        'handleTask',
        's3pBlobFetch',
        'switchCurrentProject',
        'webhookCreate',
        'webhookDelete',
        'configurationUpdate',
        'driverUpload',
        'workSpace'
    ]

    def get_params(self, page=0):
        return {"size": 500, "offset": page, "recordType": self.RECORD_TYPES}

    @property
    def path(self):
        return f"/audit"