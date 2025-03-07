from fasthtml.starlette import StreamingResponse
from fasthtml.common import to_xml
from .sse import SSE_HEADERS, ServerSentEventGenerator
#from typing import override
from fasthtml.common import *


class FastHTMLDatastarSSEResponse(StreamingResponse):
    """FastHTML-specific SSE response for DataStar integration.
    
    This class extends StreamingResponse to handle XML conversion for FastHTML components
    and provides integration with DataStar's SSE functionality.
    """
    def __init__(self, generator, *args, **kwargs):
        kwargs["headers"] = SSE_HEADERS
        
        class XMLSSEGenerator(ServerSentEventGenerator):
            @classmethod
            def merge_fragments(cls, fragments, *args, **kwargs):
                # Handle both single components and lists
                if not isinstance(fragments, list):
                    fragments = [fragments]
                
                xml_fragments = [
                    f if isinstance(f, str) else to_xml(f)  
                    for f in fragments
                ]
                return super().merge_fragments(xml_fragments, *args, **kwargs)
        
        super().__init__(generator(XMLSSEGenerator), *args, **kwargs)
