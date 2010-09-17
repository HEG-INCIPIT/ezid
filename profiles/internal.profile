# Format:
#
# element: ...
# displayname: ...
# tooltip: ...
# ... XHTML content ...
#                        <-- 1+ blank lines
# element:
# etc.

element: _urlform
displayname: URL form
tooltip:
<b><u>URL form of identifier</u></b><br/>
The identifier expressed as a URL.  Following this URL in a browser
will redirect to the object location URL.  Thus, include this URL
wherever a persistent hyperlink to the identified object is
desired.<br/>
In citations, a common practice is to display the identifier as a
hyperlink, with the identifier as the visible hyperlink text and the
URL form of the identifier as the link.  In HTML, this takes the
form<br/>
&nbsp;&nbsp;<font face="Courier">&lt;a href="url
form"&gt;identifier&lt;/a&gt;</font>

element: _target
displayname: URL
tooltip:
<b><u>Object location URL</u></b><br/>
The current location (URL) of the identified object.

element: _profile
displayname: Profile
tooltip:

element: _owner
displayname: Owner
tooltip:
<b><u>Owner</u></b><br/>
The identifier's owner.  Only the owner may modify the identifier.

element: _ownergroup
displayname: Owner group
tooltip:
<b><u>Owner group</u></b><br/>
The identifier's owner group.

element: _created
displayname: Created
tooltip:
<b><u>Created</u></b><br/>
The UTC date and time the identifier was created.

element: _updated
displayname: Updated
tooltip:
<b><u>Updated</u></b><br/>
The UTC date and time the identifier was last updated.

element: _shadowedby
displayname: Shadow ARK
tooltip:
<b><u>Shadow ARK</u></b><br/>
An independent but related ARK identifier.  The shadow ARK has the
same owner and citation metadata as this identifier, but may have a
different object location.  It may be used to provide, for example,
resolution to subcomponents of the identified object.

element: _shadows
displayname: Shadowed identifier
tooltip:
<b><u>Shadowed identifier</u></b><br/>
This identifier is a "shadow ARK" that shadows another identifier.  A
shadow ARK has the same owner and citation metadata as the shadowed
identifier, but may have a different object location.  It may be used
to provide, for example, resolution to subcomponents of the identified
object.
