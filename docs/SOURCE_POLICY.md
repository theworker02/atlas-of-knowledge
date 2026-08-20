# Source and licensing policy

Atlas is not a web scraper. Discovery reads only named, small catalog feeds listed in `sources/source-policy.json`. A source must be allowlisted, accessible without credentials, and carry a license compatible with Atlas's intended reuse before it can enter the approved registry.

## Decisions

`CC BY 4.0` and `CC0 1.0` are presently compatible for original, attributed structured transformation. NC, ND, unknown, or conflicting licenses are quarantined. Public access is never a license decision.

MIT OpenCourseWare is an excellent discovery reference, but its materials are CC BY-NC-SA 4.0 and are therefore **reference-only/quarantined** under the current commercial-compatible policy. Open Yale Courses is likewise **reference-only/quarantined** because its materials are generally CC BY-NC-SA 3.0 and may include excluded third-party rights. UC Berkeley's official catalog is included only for **metadata discovery** until a specific course's reuse rights are verified. The Open Computing Facility is not a course catalog and is not an Atlas source.

Harvard Online, Stanford Online, Carnegie Mellon OLI, and Open University OpenLearn are verified discovery sources. They are **not ingestible under the current policy**: Harvard restricts course-content use; Stanford has no verified blanket compatible reuse grant; OLI courseware is governed by platform terms; and OpenLearn is generally CC BY-NC-SA with third-party exceptions. The collector records and quarantines them automatically rather than treating a course page as permission to reuse material.

The registry records source identity, URL, license, attribution requirements, timestamp, quality decision, and ingestion state. Source material and provenance stay separate from released records. Atlas never republishes extracted source passages as its dataset content.

## Removal

Report a source, license, attribution, privacy, or accuracy issue through the private security process or a data-removal issue. We quarantine the affected source, trace its provenance, remove affected release artifacts, and publish a corrected version.
