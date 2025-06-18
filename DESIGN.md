# Design Document: Call Roster Generator

## Project Overview

This app is intended to automate the creation of balanced, fair, and constraint-aware work rosters. While the initial use case focuses on hospital on-call rosters, the logic should be able to extend school timetables, theatre suite assignments, or any environment requiring multi-variable scheduling.

SECTIONS:

- Roles and Access Control
- Data Input and Processing
- **Roster Generation Algorithm (MAIN FOCUS AT EARLY STAGE)**
- Data Output
- DIY Mode
- Privacy & Security (for later consideration)

## Roles & Access Control

A key architectural feature of the Call Roster Generator is role-based access control, ensuring that users can interact with the system according to their responsibilities and permissions. Designed with flexibility and future scalability in mind.

### Roles

- **Admin (Coordinator):**

  - Has full control over the roster group.
  - Can upload and edit the input data (e.g. CSV files).
  - Can configure constraints and generation rules.
  - Has access to encrypted name mappings if aliases are used.
  - Can upload historical metadata to balance shift assignments over time.
  - Manages visibility and access for other users.

- **Contributors (Participants):**

  - Can submit personal preferences and constraints (e.g. unavailable dates, shift preferences).
  - May only view their own submitted data.
  - Do not have access to sensitive metadata or full datasets.
  - Later stage in development might be able to request and initialise roster swaps.

- *Viewers (E.g. Switchboard, Ward Managers):*

  - Perhaps a later feature if used widely
  - Might be granted read-only access to the final generated schedules.

#### Room Keys & Group Membership

- Later plan if becomes more widely used
- Each roster group is associated with a unique alphanumeric **Room Key** E.g. FE3T (Arrangements: 1,679,616).
- Participants use this key to join a specific scheduling group, contributing their preferences securely.
- The system ensures keys are unique and logs which have been used.
- Room Keys allow the system to scale to multiple independent groups while maintaining data separation.


## Data Input and Preprocessing

The system is designed to handle structured input from multiple roles, primarily the **Admin** and later: optionally, individual **Contributors**

#### Roles & Permissions

- **Admin**:

  - Can upload full datasets
  - Controls user anonymization alias keys
  - Has access to edit core parameters (e.g. global constraints, hours, experience levels)
  - Manages who has access to submit preferences

- **Contributor (optional if appropriate)**:

  - Can submit individual preferences using a unique key or room code
  - Cannot view others' data or the anonymization key
  - Cannot override admin-set constraints

#### Data Input Format

- **CSV Uploads (primary method):**  
  Will need a good CSV example or a form where admin can set global constraints for the roster. Could be: form generates a clear CSV example that the admin can then populate. Admin then processes and uploads a structured CSV file that contains rows for each person and columns for attributes such as:

  - Alias (optional, if anonymized for the web app)
  - Availability (start and end date availability E.g. leave)
  - Roles (e.g. senior/junior)
  - Constraints (e.g. preferences on days)
  - Relationship to other persons (e.g. possible partner constraints)

- **Manual Entry Interface (future enhancement):**  
  A form-based input option for smaller teams or testing, allowing manual input instead of uploading a file.

- **Collaborative Preference Submission:**  
  Optional interface where contributors login (for their acc access and so they do not enter or edit preferences of others) enter a key (for the roster access) to submit personal preferences. These are stored under their alias and merged by the admin during processing. Could also be put on google sheets e.g. for contributors to edit and add to... (Might add an element of transpacerany so requests are more reasonable.)

- **Previous Metadata Input:**  
  The admin can optionally input prior scheduling metadata to promote fairness over time, such as:
  - Tracking past long weekend or holiday shifts to avoid repeated assignment to the same individuals
  - Check how many preferences were previously given to each person - in case there is a clash, the same person should not always get priority
  - Balancing total hours worked over multiple rosters to correct unfair distributions

#### Anonymization

- To protect privacy, especially in public or semi-public use:
  - Names are replaced with aliases (e.g. A, B, C)
  - The mapping key is known only to the Admin and not stored in the database
  - This ensures ethical handling of sensitive data when running on shared systems
  - Could also make rostering and edits more unbiased before decryption
  - Especially in healthcare facilities this is important to think about implications if full rosters with names are outputted to public erroneously

#### Preprocessing Steps

- Validate CSV input: check for formatting errors or missing fields - set value for explicitly empty fields
- Normalize data: ensure consistent representation of roles, days, hours, and boolean flags
- Encrypt to aliases (Or perhaps this is done before?)
- Index and tag rows for easier processing in the roster generation algorithm

## Roster Generation Algorithm

This core backend component is responsible for producing optimized, fair, and constraint-compliant rosters based on the processed input data.

#### Key Objectives

- Fill required shifts and time slots with the appropriate number of personnel
- Respect all global requirements of roster:

  - No. staff per day, start-stop times, experience required
  - Calculation of hours worked (post-call subtacted?)

- Respect individual requirements:

  - Maximum and minimum working hours
  - Leave days, religious observances
  - Post-call "cool-off" period - rested before next call
  - Seniority requirements (e.g., pairing juniors with seniors)
  - Sick cover

- Inter-person consideration:

  - Pair-up experience levels
  - Partners may wish not to work concurrently

- Consideration of preferences:

  - Request for specific day/weekend
  - Request for NOT specific day/weekend (How many requests viable?)
  - Weekend preference: FRI/SUN, SAT or None

- Support “soft constraints” where some preferences can be violated with penalties
- Ensure equitable distribution of workload over multiple scheduling periods (if metadata is entered)
- Generate multiple alternative rosters for comparison and selection

#### Actual Algorithm

- [Watch this space]

## Output & Presentation

Once a roster is successfully generated, it should be made easily accessible and understandable for end-users.

#### Output Formats

- **On-screen display**:
  - Clean, readable tabular format in calendar
  - Would be nice to have drop-drag editability (later stage) with live updated metadata
  - Separate views for administrators vs. individual users?
- **Downloadable files**:
  - Export roster as `.csv`, `.xlsx`, or `.pdf`
  - Option to export metadata summary with statistics
- **Printable version**:
  - Printer-friendly layout for distribution
  - This would have to be de-crypted again... User should be able to do that somehow. (Will have to be decrypted for use otherwise some users might keep it encrypted and just paste a key underneath. That will be a nightmare to read.)

#### Metadata & Fairness Reports

- Provide summary statistics alongside each generated roster:
  - Total hours worked per person*
  - Weekend/holiday distribution*
  - Preference satisfaction rate
  - Hours recovered or adjusted from previous cycles*
  - Specify which preferences were not granted
- Optional feedback module to rate the quality of the generated roster
- *These statistics would ideally be available to users as well somehow if they want. Other more sensitive preferences could be kept as admin only.


## DIY Mode

Perhaps some admins like the autonomy of making rosters manually. It would be a nice option to be able to facilitate this by the following:
- Have a way to input global constraints (E.g. number of participants, shift hours and days, number needed per shift etc)
- Could still have a way to add all the preferences that might be visible for admin
- Initialising this information into an empty calendar that has slots to be filled on the different days. 
- Admin can then drag-drop different names/aliases into different slots
- Some metadata could then be updated live (e.g. hours worked per person)
- Can have options for names to light up in different colours (E.g. red if a person is scheduled during their leave, orange if they are working on a requested off day, blue if they are exceeded maximum hours etc)
- Could be more user-friendly and flexible for some users

## Security & Privacy

-