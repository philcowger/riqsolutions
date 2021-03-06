"""Query Module for the RiskIQ Solutions Python API Library"""

from .riskiqapi import RiskIQAPI
from riqsolutions.riskiqapi.workspace import Workspace
from riqsolutions.riskiqapi.facets import Facet
from riqsolutions.riskiqapi.comparators import Comparator
from riqsolutions.riskiqapi.values import Value
from riqsolutions.cli import configure_api
import json

class Query(RiskIQAPI):
    """
    Represents a Query against the Global Inventory API
    """
    def __init__(self, api_token=None, api_key=None, context=None):
        super().__init__(
            api_token, 
            api_key, 
            context,
            url_prefix='v1/globalinventory', 
            hostname='api.riskiq.net'
            )
        self._fullQuery=[]
        self._EC = 0

    def get_query(self):
        """
        Returns the current Query object

        :returns: self._fullQuery
        """
        return self._fullQuery

    def get_facets(self):
        this_f = Facet()
        return this_f.get_facets()
    
    def get_comparators(self):
        this_f = Comparator()
        return this_f.get_comparators()

    def add(self, facet=None, comparator=None, value=None):
        """
        Add a single statement (facet, comparator, value) to a query object

        :param facet: type str or Facet(), required
        :param comparator: type str or Comparator(), required
        :param value: type str or Value(), required
        """
        this_f = Facet()
        this_f.facet = facet

        this_c = Comparator()
        this_c.comparator = comparator

        this_v = Value(self)
        if this_f.facet.lower() == 'alexabucket':
            this_v.alexaBucket = value
        elif this_f.facet.lower() in ['type','assettype']:
            this_v.assetType = value
        elif this_f.facet == 'brand':
            this_v.brand = value
            if type(value) == list:
                _tl = []
                for _v in this_v.value:
                    for k, v in _v.items():
                        _tl.append(k)
                this_v.value = _tl
            else:
                for k, v in this_v.value.items():
                    this_v.value = k
        elif this_f.facet == 'confidence':
            this_v.confidence = value
        elif this_f.facet == 'domainExpiration':
            this_v.domainExpiration = value
        elif this_f.facet in ['org','organizatin']:
            this_v.org = value
            if type(value) == list:
                _tl = []
                for _v in this_v.value:
                    for k, v in _v.items():
                        _tl.append(k)
                this_v.value = _tl
            else:
                for k, v in this_v.value.items():
                    this_v.value = k
        elif this_f.facet == 'portLastSeen':
            this_v.portLastSeen = value
        elif this_f.facet == 'portState':
            this_v.portState = value
        elif this_f.facet == 'priority':
            this_v.priority = value
        elif this_f.facet == 'removedState':
            this_v.removedState = value
        elif this_f.facet == 'sslCertExpiration':
            this_v.sslCertExpiration = value
        elif this_f.facet == 'state':
            this_v.state = value
        elif this_f.facet == 'tag':
            this_v.tag = value
            if type(value) == list:
                _tl = []
                for _v in this_v.value:
                    for k, v in _v.items():
                        _tl.append(k)
                this_v.value = _tl
            else:
                for k, v in this_v.value.items():
                    this_v.value = k
        elif this_f.facet == 'validationType':
            this_v.validationType = value
        else:
            this_v.rando = value
        
        self._EC += 1
        self._fullQuery.append(
            {'expressionId':self._EC,'operator':'and','facet':this_f.facet,'comparator':this_c.comparator,'value':this_v.value}
        )
        
    
    def _and(self, facet=None, comparator=None, value=None):
        self._EC += 1
        self._fullQuery.append(
            {'expressionId':self._EC,'operator':'and','facet':facet,'comparator':comparator,'value':value}
        )
    
    def _or(self, facet=None, comparator=None, value=None):
        self._EC += 1
        self._fullQuery.append(
            {'expressionId':self._EC,'operator':'or','facet':facet,'comparator':comparator,'value':value}
        )

    def remove(self, id):
        """
        Remove a single statement (facet, comparator, value) from the current query object
        
        :param id: type int, required
        """
        if type(id) is not list:
            for e in self._fullQuery:
                if e['expressionId'] == id:
                    self._fullQuery.remove(e)
        else:
            for this_id in id:
                for e in self._fullQuery:
                    if e['expressionId'] == this_id:
                        self._fullQuery.remove(e)
                
            
    def run(self, size=1000, idsOnly=False):
        """
        Executes the current query object

        https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_search
        
        :param size: type int, optional (default:1000)
        :param idsOnly: type bool, optional (default: False)
        """
        
        this_payload = process_query_object(self)
        full_response = []
        this_mark = '*'
        count=0
        while True:
            this_params = {
                'global':False,
                'size':size,
                'mark':this_mark,
                'idsOnly':idsOnly
            }
            r = self.post('search', payload=this_payload, params=this_params)
            if type(r) == list and 'error' in r.keys():
                if count >= 5:
                    raise ValueError('Query().run failed too many times on the same mark bundle')
                else:
                    count += 1
            else:
                count = 0
                this_data = r.json()
                for c in this_data.get('content'):
                    full_response.append(c)
                if this_data.get('last') != True:
                    this_mark = this_data.get('mark')
                else:
                    return {'results':full_response}


def process_query_object(self):
    values = []
    for e in self._fullQuery:

        this_v = {
            'name':e['facet'],
            'operator':e['comparator'],
            'value':e['value']
        }
        values.append(this_v)

    this_payload = {
        'query':None,
        'filters': {
            'condition':'AND',
            'value':values
        }
    }
    return this_payload
