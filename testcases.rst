**TEST CASE: /id**

`Descriptions:`
    Show the cluster peers and its daemon information
    GET

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET operation without any arguments.(1)Create session without verbose argument. http://i.storswift.com:9194/id (2)Create session without verbose argument but with other letters. http://i.storswift.com:9194/idid
     - (1)Response 200 code and body right.(2)Response 404 code.
     - A
   * - 3
     - GET method with error arguments. Create session with error arguments' strings. Eg. verbos=1.
     - Response 200 code.
     - A
   * - 4
     - Repeat step 1, 2, 3 on another node.
     - Result 1, 2, 3.
     - A
   * - 5
     - Function: GET check id result. Then a new node add into ipfs-cluster. Check the api again.
     - 200 code. A new peer in the result. Filed name: "cluster_peers".
     - M

**TEST CASE: /peers**

`Descriptions:`
    List the cluster servers with open connections.
    GET method.

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - No arguments. (1) Create session without verbose argument. (2)Create session without verbose argument & with other api interface.
     - (1)Response 200 code and body right. (2)Response 404 code.
     - A
   * - 2
     - With verbose argument. (1) Create session with verbose argument and value is 0,1,true and false, respectively. (2) Create session with verbose argument and value null. (3) Create session with verbose argument and error value(non-bool). (4) Create session with verbose argument and other strings.
     - (1)Response 200 code and body right. (2)Response 200 code. (3)Response 200 code. (4)Response 200 code.
     - A
   * - 3
     - GET method with error arguments. Create session with error arguments' strings. Eg. verbos=1.
     - Response 200 code.
     - A
   * - 4
     - Repeat step 1, 2, 3 on another node.
     - Result 1,2,3.
     - A
   * - 5
     - Function: GET check the api result. Then a new node add into ipfs-cluster. Check the api result again.
     - 200 code. A new peer in the result. Filed name: "cluster_peers".
     - M

**TEST CASE: /peers/{peerID}**

`Descriptions:`
    Remove a cluster peer from the cluster.
    DELETE

`Preparation:`
    IPFS-cluster with some nodes. Get each peer ID

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - (1) Create session without "peerID" argument. http://i.storswift.com:9194/peers (2) Create session with error "peerID" argument.http://i.storswift.com:9194/peers/xxxx (3) Create session with error log string.http://i.storswift.com:9194/peers/x (4) Convert the peerid to capital letters. Then DELETE.
     - (1) Error code. 404. (2) Error code. 400.{"code": 400,"message": "error decoding Peer ID: uvarint: buffer too small"} (3) {"code": 400, "message": "error decoding Peer ID: multihash length inconsistent:" } (4)204 code. No peer will be removed.
     - M
   * - 2
     - With correct argument and value. (1) Create session with required argument and correct value. Check peers. (2) DELETE the peerID again.(This step equal delete a peer which not exist but id is regular correct QmW8vdqrNj86rbW6RnWTUnFFD1XcHrUws3rv4GGbiNR7cx)
     - (1) 204 code and correct body. The peer be removed. (2) 204 code.
     - M
   * - 3
     - Repeat step 1, 2 on another node.
     - Result 1,2.
     - M

**TEST CASE: /pins**

`Descriptions:`
    List current status of pins in the cluster.
    GET

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Create session without any parameters. (1) GET when no pins. (2) GET when exist pins. (3) GET use the error api strings, eg. /pinss.
     - (1) 200 code and body is []. (2) 200 code and body correct. (3) 404 code.
     - A
   * - 2
     - Wth verbose parameter. (1) Use correct bool value. 0/1/true/false. (2) Use error value. XXX, 34, "2" and so on.
     - 200 code and body correct.
     - A
   * - 3
     - With quiet parameter. (1) Use correct bool value. (2) Use error value.
     - 200 code.
     - A
   * - 4
     - With combined parameters. Use verbose and quiet parameters with correct values. Use correct verbose value and error quiet value. Use correct quiet value and error verbose value.
     - 200 code.
     - A
   * - 5
     - Repeat step 1, 2, 3, 4 on another node.
     - Result 1-4.
     - A
   * - 6
     - Function: Add files and generate "pinned", "pin_err" record.
     - Check api result. It contains correct pin status.
     - M

**TEST CASE: /pins/{cid}/sync**

`Descriptions:`
    Sync local status from IPFS.
    POST

`Preparation:`
    IPFS-cluster with some nodes. A pins file cid.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Create session with correct cid.
     - 200 code and body correct.
     - A
   * - 2
     - Create session with incorrect cid.
     - 400 code. {"code":400,"message":"error decoding Cid: selected encoding not supported"}
     - A
   * - 3
     - Create without cid. curl -X POST http://10.10.165.11:9094/pins/sync
     - 200 code. Body is [].
     - A
   * - 4
     - On another node create session with another cid.
     - 200 code.
     - M
   * - 5
     - Check cid string from step 1 on different node.
     - Correct.
     - M
   * - 6
     - Function: use a cid post the api.
     - Check the result. In peer map, each peer has correct status.
     - M

**TEST CASE: /pins/{cid}/recover**

`Descriptions:`
    Recover a CID.
    POST

`Preparation:`
    IPFS-cluster with some nodes. A pins file cid.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Create session with correct cid string.
     - 200 code and body correct.
     - A
   * - 2
     - Create session with incorrect cid string.
     - 400 code.
     - A
   * - 3
     - Create session without cid string.
     - 400 code.
     - A

**TEST CASE: /pins/recover**

`Descriptions:`
    Attempt to re-pin/unpin CIDs in error state.
    POST

`Preparation:`
    IPFS-cluster with some nodes. A pins file cid.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Create session without any cid string.
     - 400 code.
     - A
   * - 2
     - Create session with local=true.
     - 200 code and body correct.
     - A
   * - 3
     - Create session with local=false.
     - 400 code.
     - A
   * - 4
     - Create an error cid state. Create session with local=true then check the pins status.
     - 200 code and status correct.
     - M

**TEST CASE: /api/v0/uid/new**

`Descriptions:`
    Create a unique UID and peer ID pair from Hive cluster.
    The UID can be used to identify endpoints in communication， the PeerID is a virtual IPFS peer ID.

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET the interface.
     - 200 code and body correct.
     - A
   * - 2
     - GET the interface again.
     - 200 code and a new id and peerid.
     - A
   * - 3
     - GET the interface with extra argument.
     - 200 code and new uid.
     - A
   * - 4
     - Function: GET api 10 times, check each new id different.
     - Successful.
     - A
   * - 5
     - Function: (1) Use old id mkdir /old_uid_mk and add a file. (2) Generate a new id and peerid. (3) Another node use the new peer id check the directory tree.
     - Operations successful. New peerid cannot get the directory tree.
     - A

**TEST CASE: /api/v0/uid/login**

`Descriptions:`
    Log in to Hive Cluster using the UID you created earlier.

`Preparation:`
    IPFS-cluster with some nodes.
    Generate an uid.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without any uid value.
     - 500 code and body correct. {"Message":"error reading request: /api/v0/uid/login"}
     - A
   * - 2
     - GET with error uid value.
     - 500 code and body correct. {"Message":"IPFS unsuccessful: 500: no key named xxxx was found"}
     - A
   * - 3
     - GET with error argument.
     - 500 code and body correct. {"Message":"error reading request: /api/v0/uid/login?uidd=xxxx"}
     - A
   * - 4
     - GET with correct uid.
     - 200 code and body correct.
     - A
   * - 5
     - Function: (1) Create new id and peerid. (2) Create some directory and add some files. (3) GET/POST the api. can generate new id. (4) Use new id check the directory and file view tree on another node.
     - (1) Operation successful. (2) Operation successful. (3) Operation successful. New id should different from old id. (4) Can get the view tree.
     - A

**TEST CASE: /api/v0/file/pin/add**

`Descriptions:`
    Pin objects in the cluster.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.
    Add some files and remember the hash values.
    Add a directory with some files.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET and POST the api without any parameters.
     - 500 code. {"Message": "Error parsing CID: selected encoding not supported"}
     - A
   * - 2
     - GET and POST the api with correct arg string.
     - 200 code.
     - A
   * - 3
     - GET and POST the api with another arg string which not exist but comply the hash regular.
     - 200 code and body correct.
     - A
   * - 4
     - GET and POST the api with another arg string which not exist and not comply the hash regular, eg. xxxxx.
     - 500 code. {"Message": "Error parsing CID: selected encoding not supported"}
     - A
   * - 5
     - GET and POST the api with "recursive" is 0/false. (1) pin add a file. (2) pin add a directory.
     - 200 code.
     - A
   * - 6
     - GET and POST with "hidden" is 1/true.
     - 200 code.
     - A
   * - 7
     - POST and GET with correct joint parameter. Eg. recursive=1&hidden=1.
     - 200 code.
     - A
   * - 8
     - POST and GET with correct joint parameter. But some of them value incorrect. Eg. recursive=directxxx&hidden=1
     - 200 code.
     - A
   * - 9
     - POST and GET with joint parameter. But some of parameter incorrect. Eg. recursive=1&hiddenxx=1
     - 200 code.
     - A


**TEST CASE: /api/v0/file/pin/ls**

`Descriptions:`
    List objects that pinned to the cluster.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.
    Add some files and remember the hash values.
    Create some different status of pin, "direct", "indirect", "recursive".

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - POST and GET without any parameter.
     - 200 code and body correct.
     - A
   * - 2
     - POST and GET with "type" and the value is "direct", "indirect", "recursive", "all" respectively.
     - 200 code and return result correct.
     - A
   * - 3
     - POST and GET with "quiet". Each bool value respectively.
     - 200 code.
     - A
   * - 4
     - POST and GET with correct joint parameter. Eg. type=direct&quiet=1.
     - 200 code.
     - A
   * - 5
     - POST and GET with correct joint parameter. But some of them value incorrect. Eg. type=directxxx&quiet=1
     - 200 code.
     - A
   * - 6
     - POST and GET with joint parameter. But some of parameter incorrect. Eg. type=direct&qxxxxuiet=1
     - 200 code.
     - A


**TEST CASE: /api/v0/file/pin/rm**

`Descriptions:`
    Remove pinned objects from the cluster.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.
    Add some files and remember the hash values.
    Create some different status of pin, "direct", "indirect", "recursive".

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - POST and GET without any parameter. http://10.10.165.11:9095/api/v0/pin/rm
     - 500 code. {"Message":"Error: bad argument"}
     - A
   * - 2
     - GET with an error hash value. http://10.10.165.11:9095/api/v0/pin/rm?arg=xxxxxx
     - 500 code. {"Message":"Error parsing CID: selected encoding not supported"}
     - A
   * - 3
     - GET with correct hash value.
     - 200 code. Then check status correct.
     - A
   * - 4
     - POST with an unpin hash.
     - 500 code. {"Message":"cannot unpin pin uncommitted to state: cid is not part of the global state"}
     - A
   * - 5
     - POST with an correct hash.
     - 200 code.
     - A
   * - 6
     - GET with recursive and correct value.
     - 200 code.
     - A
   * - 7
     - POST with recursive and incorrect value.
     - 200 code.
     - A
   * - 8
     - GET with error parameter string. Eg. recursivxxx
     - 200 code.
     - A

**TEST CASE: /api/v0/file/add**

`Descriptions:`
    Add a file or directory to cluster.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.


`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without any parameter. http://10.10.165.11:9095/api/v0/file/add
     - 500 code. {"Message":"error reading request: request Content-Type isn't multipart/form-data"}
     - A
   * - 2
     - GET with required argument "path".
     - 200 code and add file successful. Return body correct.
     - A
   * - 3
     - GET required argument "path", but file not exist.
     - Return fail message.
     - A
   * - 4
     - GET a random string of "path".
     - Return fail message.
     - A
   * - 5
     - GET with correct value of "recursive".
     - 200 code.
     - A
   * - 6
     - POST and GET with incorrect value of "recursive".
     - 500 code.
     - A
   * - 7
     - POST and GET with correct value of "hidden".
     - 200 code.
     - A
   * - 8
     - POST and GET with incorrect value of "hidden".
     - 500 code. {"Message":"error parsing options:parameter recursive invalid"}
     - A
   * - 9
     - GET with error parameter string. Eg. recursivxxx
     - 500 code. {"Message":"error parsing options:parameter recursive invalid"}
     - A
   * - 10
     - POST and GET with correct joint parameter.
     - 200 code.
     - A
   * - 11
     - POST and GET with correct joint parameter. But some of them value incorrect.
     - 200 code.
     - A
   * - 12
     - POST and GET with joint parameter. But some of parameter incorrect.
     - 200 code.
     - A

**TEST CASE: /api/v0/file/cat**

`Descriptions:`
    cat files content from the hive cluster
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.


`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without arg argument.
     - 500 code.
     - A
   * - 2
     - GET with an error hash code for arg.
     - 500 code.
     - A
   * - 3
     - GET with an un-exist hash code for arg.
     - 500 code.
     - A
   * - 4
     - GET with correct hash value.
     - 200 code.
     - A

**TEST CASE: /api/v0/file/get**

`Descriptions:`
    Download files from the cluster.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.


`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 500 code.
     - A
   * - 2
     - GET with correct "arg" argument.
     - 200 code and body correct.
     - A
   * - 3
     - GET with error "arg" value. Eg. xxxx
     - 500 code.
     - A
   * - 4
     - GET with correct "arg" argument ,value correct but not exist.Eg. QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQh
     - Timeout and error.
     - A
   * - 5
     - GET with "output" argument.
     - <Discard in current version.>
     - M
   * - 6
     - GET with "archive" argument.
     - <Discard in current version.>
     - M
   * - 7
     - GET with "compress" argument with correct bool value.
     - 200 code.
     - A
   * - 8
     - GET with "compress" argument with incorrect bool value.
     - 500 code.
     - A
   * - 9
     - GET with "arg", "compress" and "compress-level" arguments with correct value.
     - 200 code.
     - A
   * - 10
     - GET with "arg", "compress" and "compress-level" arguments but level value not in 1-9.
     - 500 code. {"Message":"compression level must be between 1 and 9","Code":0,"Type":"error"}
     - A
   * - 11
     - GET with "arg" and "compress-level" arguments only
     - 200 code.
     - A

**TEST CASE: /api/v0/file/ls**

`Descriptions:`
    List directory contents for Unix filesystem objects.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.


`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET and POST without required argument.
     - 400 code.
     - A
   * - 2
     - GET and POST with correct "arg" argument and value.
     - 200 code and body correct.
     - A
   * - 3
     - GET and POST with correct "arg" argument and error value.
     - 500 code. {"Message":"invalid 'ipfs ref' path","Code":0,"Type":"error"}
     - A

**TEST CASE: /api/v0/files/cp**

`Descriptions:`
    Copy files among clusters.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.


`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 500 code. {"Message":"error reading request: /api/v0/files/cp"}
     - A
   * - 2
     - GET only with uid argument.
     - 500 code. {"Message":"error reading request: /api/v0/files/cp?uid=uid-e3923bb6-526f-46ef-9c98-2bff329f0c57"}
     - A
   * - 3
     - GET with correct uid, source and dest argument.
     - 200 code.
     - A
   * - 4
     - GET with error source value, with correct uid and dest.
     - 500 code.
     - A
   * - 5
     - GET with error dest value, with correct uid and source.
     - 200 code.
     - A
   * - 6
     - GET with random dest value. Example: /xxsssxxx
     - 200 code.
     - A


**TEST CASE: /api/v0/files/flush**

`Descriptions:`
    Flush a given path’s data to cluster.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 500 code. {"Message":"error reading request: /api/v0/files/flush"}
     - A
   * - 2
     - GET with an error uid string.
     - 500 code. {"Message":"IPFS unsuccessful: 500: file does not exist"}
     - A
   * - 3
     - GET with "path" string which not / and not exist.
     - 500 code. {"Message":"error reading request: /api/v0/files/flush?path=/"}
     - A
   * - 4
     - Make a directory and add a file. GET with path argument.
     - 200 code. Body correct.
     - A

**TEST CASE: /api/v0/files/ls**

`Descriptions:`
    List directories in the private mutable namespace.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET with required argument.
     - 200 code. Eg: {"Entries":[{"Name":"suxx","Type":0,"Size":0,"Hash":""},{"Name":"suxx2","Type":0,"Size":0,"Hash":""}]}
     - A
   * - 2
     - GET with "uid" argument.
     - 200 code.
     - A
   * - 3
     - GET with "uid" but value is error.
     - 500 code. {"Message":"IPFS unsuccessful: 500: file does not exist"}
     - A
   * - 4
     - GET only with "path" argument. The value is an exist directory.
     - 500 code.
     - A
   * - 5
     - GET without any arguments.
     - 500 code. {"Message":"error reading request: /api/v0/files/ls"}
     - A

**TEST CASE: /api/v0/files/mkdir**

`Descriptions:`
    Create directories.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 400 code.
     - A
   * - 2
     - GET with "path"(arg) argument only but string is error.
     - 500 code. {"Message":"error reading request: /api/v0/files/mkdir?arg=dir1"}
     - A
   * - 3
     - GET with "uid" argument only.
     - 200 code.
     - A
   * - 4
     - GET with correct "path" argument and value with uid.
     - 200 code.
     - A
   * - 5
     - GET with correct "path" argument and value with an exist uid.
     - 500 code. {"Message":"IPFS unsuccessful: 500: file already exists"}
     - A

**TEST CASE: /api/v0/files/mv**

`Descriptions:`
    Move files.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 500 code.
     - A
   * - 2
     - GET with "source" argument only.
     - 500 code.
     - A
   * - 3
     - GET with "dest" argument only.
     - 500 code.
     - A
   * - 4
     - GET with "source" and "dest" value but without uid.
     - 500 code.
     - A
   * - 5
     - GET with "uid" argument only.
     - 500 code.
     - A
   * - 6
     - GET with uid, source, dest argument but values error.
     - 500 code.
     - A
   * - 7
     - GET with uid, source, dest argument and correct value.
     - 200 code.
     - A


**TEST CASE: /api/v0/files/read**

`Descriptions:`
    Read a file in a given path.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 500 code.
     - A
   * - 2
     - GET only with uid argument.
     - 500 code.
     - A
   * - 3
     - GET only with path argument.
     - 500 code.
     - A
   * - 4
     - GET with error path argument with correct uid.
     - 500 code.
     - A
   * - 5
     - GET with correct path and uid.
     - 200 code.
     - A
   * - 6
     - GET with correct offset and count value.
     - 200 code.
     - A


**TEST CASE: /api/v0/files/rm**

`Descriptions:`
    Remove a file.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 500 code.
     - A
   * - 2
     - GET method rm a directory.
     - 500 code. {"Message":"/suxx is a directory, use -r to remove directories","Code":0,"Type":"error"}
     - A
   * - 3
     - GET rm an un-exist file.
     - 500 code. {"Message":"file does not exist","Code":0,"Type":"error"}
     - A
   * - 4
     - GET with uid and a file.
     - 200 code.
     - A
   * - 5
     - GET with recursive argument.
     - 200 code.
     - A


**TEST CASE: /api/v0/files/stat**

`Descriptions:`
    Display file status.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.
    Make some directory.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 500 code. {"Message":"error reading request: /api/v0/files/stat"}
     - A
   * - 2
     - GET with "path" with error directory value with correct uid.
     - 500 code.{"Message":"file does not exist","Code":0,"Type":"error"}
     - A
   * - 3
     - GET with "path" with correct directory value but without uid value.
     - 500 code.
     - A
   * - 4
     - GET with "format" arguments and value.
     - 200 code.
     - M
   * - 5
     - GET with correct path and uid argument.
     - 200 code.
     - A
   * - 6
     - GET with error hash argument.
     - 500 code.
     - A




**TEST CASE: /api/v0/files/write**

`Descriptions:`
    Write to a mutable file in a given filesystem.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without required argument.
     - 500 code. {"Message":"error reading request: /api/v0/files/write"}
     - A
   * - 2
     - GET with only error uid value
     - 500 code.
     - A
   * - 3
     - GET with only correct uid value.
     - 500 code.
     - A
   * - 4
     - GET with correct uid and file argument but without data.
     - 500 code. {"Message":"request Content-Type isn't multipart/form-data"}
     - A
   * - 5
     - GET with correct uid, file and truncate argument.
     - 200 code. Correct body.
     - A
   * - 6
     - GET with other arguments which no must required.
     - 200 code.
     - A
   * - 7
     - GET with other arguments which no must required, but value error.
     - 500 code.
     - A

**TEST CASE: /api/v0/name/publish**

`Descriptions:`
    Publish user context file or directory to public.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET without any argument.
     - 500 code. {"Message":"error reading request: /api/v0/name/publish"}
     - A
   * - 2
     - GET with an un-exist uid argument
     - 500 code.
     - A
   * - 3
     - GET with correct "path" and "uid" value.
     - 200 code. {"Name":"QmfCKhCxwwmHAnb5m3UF7Qb1ku3f1y2ordg834r9NA5hxN","Value":"/ipfs/QmXUvoNTFCzkWY1a9SPxuERTqDhHz1NKRUF3xj1wD8iQVJ"}
     - A
   * - 4
     - GET with error uid or path
     - 500 code.
     - A
   * - 5
     - Make cluster only one node.
     - GET with correct "path" and "uid" value.
     - 500 code. {"Message":"invalid 'ipfs ref' path","Code":0,"Type":"error"}
     - M

**TEST CASE: /api/v0/message/pub**

`Descriptions:`
    Publish a message to a given pubsub topic.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Temporary unrealized
     - Temporary unrealized
     - A

**TEST CASE: /api/v0/message/sub**

`Descriptions:`
    Subscribe to message to a given topic.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Temporary unrealized
     - Temporary unrealized
     - A


**TEST CASE: /version**

`Descriptions:`
    Version information.
    GET, POST

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - GET and POST without any argument.
     - 200 code. Body correct. {"Version":"0.8.0+git0581a90b0ece7858198b6fc82a369cd61b65e407"}
     - A
   * - 2
     - GET and POST with "number" correct argument.
     - 200 code. Body correct.
     - A
   * - 3
     - GET and POST with "number" incorrect argument.
     - 200 code. Body correct.
     - A
   * - 4
     - GET and POST with "commit" correct argument.
     - 200 code. Body correct.
     - A
   * - 5
     - GET and POST with "commit" incorrect argument.
     - 200 code. Body correct.
     - A
   * - 6
     - GET and POST with "repo" correct argument.
     - 200 code. Body correct.
     - A
   * - 7
     - GET and POST with "repo" incorrect argument.
     - 200 code. Body correct.
     - A
   * - 8
     - GET and POST with "all" correct argument.
     - 200 code. Body correct.
     - A
   * - 9
     - GET and POST with "all" incorrect argument.
     - 200 code. Body correct.
     - A
   * - 8
     - GET and POST with joint correct argument.
     - 200 code. Body correct.
     - A
   * - 9
     - GET and POST with joint incorrect argument.
     - 200 code. Body correct.
     - A

**TEST CASE: [PERF] /api/v0/file/add**

`Descriptions:`
    Write Performance testing.
    GET

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - On a linux node make a tmp ram-disk.
     - Successful.
     - M
   * - 2
     - Generate a valid file 10G size in the ram-disk.
     - Successful.
     - M
   * - 3
     - Use GET method add the file to ipfs-cluster. Remember the speed and time spent.
     - Successful.
     - M
   * - 4
     - Use the GET method add the file again. Remember the speed and time spent.
     - Successful.
     - M
   * - 5
     - Generate a so large file on a node more 200G. Add the so large file to ipfs-cluster.
     - Successful. Should not break off.
     - M
   * - 6
     - Create 102400 1M files.
     - Successful.
     - M
   * - 7
     - Add the files into ipfs-cluster. Remember the speed and time.
     - Successful.
     - M


**TEST CASE: [PERF] /api/v0/file/get**

`Descriptions:`
    Get Performance testing.
    GET

`Preparation:`
    IPFS-cluster with some nodes.
    On a node

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - On a linux node make a tmp ram-disk.
     - Successful.
     - M
   * - 2
     - Generate a valid file 10G size in the ram-disk.
     - Successful.
     - M
   * - 3
     - Use GET method get the file from ipfs-cluster to another file. Remember the speed and time spent.
     - Successful.
     - M
   * - 4
     - Pin the file after pinned. Get the file on the third node. Remeber the speed and time.
     - Successful.
     - M
   * - 5
     - Use the GET method get the file on another node. Remember the speed and time spent.
     - Successful.
     - M
   * - 6
     - Generate a so large file on a node more 200G. Get the so large file from ipfs-cluster on another node.
     - Successful. Should not break off.
     - M


**TEST CASE: [PERF] /api/v0/file/ls**

`Descriptions:`
    Ls Performance testing.
    GET

`Preparation:`
    IPFS-cluster with some nodes.

`Steps:`

.. list-table::
   :widths: 10 30 30 10
   :header-rows: 1

   * - No.
     - Actions
     - Expect
     - Auto/Manual
   * - 1
     - Makedir a directory, and generate 10000000 files in the directory.
     - Successful.
     - M
   * - 2
     - Add the directory and remember directory's Hash value.
     - Successful.
     - M
   * - 3
     - On another node. Ls the directory.
     - Successful. Remember the time cost.
     - M