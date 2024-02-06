import { Card, CardContent, CardHeader } from '@/components/ui/card';

export function TrainingAndWorkshopSection() {
  return (
    <section>
      <Card>
        <CardHeader className="prose max-w-none">
          <h2>Training and Workshops</h2>
          <p>
            Welcome to the Training and Workshops section of the Polytechnic
            University of the Philippines (PUP) University Research Information
            System (URIS). PUP is dedicated to enhancing research capabilities
            and skills within our academic community. Explore our upcoming
            training sessions and workshops designed to empower researchers,
            students, and faculty members:
          </p>
        </CardHeader>
        <CardContent>
          <article className="prose max-w-none mt-5">
            <h3>Research Proposal Writing Workshop</h3>

            <ul>
              <li>
                <p>
                  <strong>Description:</strong>
                </p>
                <p>
                  The Research Proposal Writing Workshop is tailored to equip
                  researchers with the knowledge and skills required to craft
                  compelling research proposals. Whether you are an experienced
                  researcher or just beginning your journey, this interactive
                  workshop will guide you through the essential elements of a
                  successful research proposal. Topics covered include research
                  design, literature review, proposal structure, and strategies
                  to increase your chances of securing research funding and
                  approvals
                </p>
              </li>

              <li>
                <p>
                  <strong>Date:</strong>
                </p>
                <p>April 29, 2024</p>
              </li>

              <li>
                <p>
                  <strong>Time:</strong>
                </p>
                <p>5:00 PM</p>
              </li>

              <li>
                <p>
                  <strong>Location:</strong>
                </p>
                <p>Acad 105</p>
              </li>

              <li>
                <p>
                  <strong>Facilitator:</strong>
                </p>
                <p>Mr. Leandro Avena IV</p>
              </li>

              <li>
                <p>
                  <strong>Registration:</strong>
                </p>
                <p>
                  To secure your spot in this workshop, please complete the
                  registration form available on the PUPQC RIS portal. We
                  encourage early registration, as seats are limited.
                </p>
              </li>
            </ul>
          </article>
        </CardContent>
      </Card>
    </section>
  );
}
